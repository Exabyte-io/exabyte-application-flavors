{#- ========== General setup ========== -#}
{%- if category == "clustering" -%}
    {% set result_ending = "labels" %}
{%- else -%}
    {% set result_ending = "predictions" %}
{%- endif -%}

{#- ========== Comment Block ========== -#}
{{ description | comment_box(documentation_box_common_text=documentation_box_common_text[category]) | safe }}

{# ========== Imports Block ========== #}
{%- for item in  imports -%}
import {{ item }}
{% endfor -%}
import sklearn.metrics
import numpy as np
import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        {# ========== Load Training Data ========== -#}
        # Restore the data
        {%- if category != "clustering" %}
        train_target = context.load("train_target")
        test_target = context.load("test_target")
        {%- endif %}
        train_descriptors = context.load("train_descriptors")
        test_descriptors = context.load("test_descriptors")

        {% if category != "clustering" %}
        # Flatten the targets
        train_target = train_target.flatten()
        test_target = test_target.flatten()
        {%- endif %}

        {#- ========== Base Estimators (Ensembles Only)! ========== #}
        {% if ensemble %}
        # Initialize the Base Estimator
        base_estimator = {{ base_estimator_class }}(
            {%- for var, arg in base_estimator_default_args.items() %}
            {{ var }}={{ arg | generate_nonetype | quoted_strings | safe }},
            {%- endfor %}
        )
        {% endif %}
        {# ========== Create and Train the Model ========== -#}
        # Initialize the Model
        model = {{ model_class }}(
                {%- for var, arg in model_default_args.items() %}
                {{ var }}={{ arg | generate_nonetype | quoted_strings | safe }},
                {%- endfor %}
                {%- if ensemble %}
                base_estimator=base_estimator,
                {%- endif %}
        )

        # Train the model and save
        model.fit(train_descriptors{% if category != "clustering" %}, train_target{% endif %})
        context.save(model, {{ name | quoted_strings | safe }})
        train_{{ result_ending }} = model.predict(train_descriptors)
        test_{{ result_ending }} = model.predict(test_descriptors)

        {# ========== Regression Training Metrics ========== -#}
        {% if category == "regression" -%}
        # Scale predictions so they have the same shape as the saved target
        train_predictions = train_predictions.reshape(-1, 1)
        test_predictions = test_predictions.reshape(-1, 1)

        # Scale for RMSE calc on the test set
        target_scaler = context.load("target_scaler")

        # Unflatten the target
        test_target = test_target.reshape(-1, 1)
        y_true = target_scaler.inverse_transform(test_target)
        y_pred = target_scaler.inverse_transform(test_predictions)

        # RMSE
        mse = sklearn.metrics.mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        print(f"RMSE = {rmse}")
        context.save(rmse, "RMSE")

        {# ========== Classification Training Metrics ========== -#}
        {% elif category == "classification" -%}
        # Save the probabilities of the model
        test_probabilities = model.predict_proba(test_descriptors)
        context.save(test_probabilities, "test_probabilities")

        # Print some information to the screen for the regression problem
        confusion_matrix = sklearn.metrics.confusion_matrix(test_target,
                                                            test_predictions)
        print("Confusion Matrix:")
        print(confusion_matrix)
        context.save(confusion_matrix, "confusion_matrix")

        {% endif -%}

        {# ========== Save the data ========== -#}
        context.save(train_{{ result_ending }}, "train_{{ result_ending }}")
        context.save(test_{{ result_ending }}, "test_{{ result_ending }}")

    # Predict
    else:
        {# ========== Predictions Block ========== -#}
        # Restore data
        descriptors = context.load("descriptors")

        # Restore model
        model = context.load({{ name | quoted_strings | safe }})

        # Make some predictions
        predictions = model.predict(descriptors)

        {% if category == "classification" %}
        # Transform predictions back to their original labels
        label_encoder: sklearn.preprocessing.LabelEncoder = context.load("label_encoder")
        predictions = label_encoder.inverse_transform(predictions)
        {% endif %}

        # Save the predictions to file
        np.savetxt("predictions.csv", predictions, header="prediction", comments="", fmt="%s")
