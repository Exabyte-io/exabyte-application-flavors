# ------------------------------------------------------------ #
# Workflow unit for a random forest classification model with  #
# Scikit-Learn. Parameters derived from Scikit-Learn's         #
# defaults.                                                    #
#                                                              #
# When then workflow is in Training mode, the model is trained #
# and then it is saved, along with the confusion matrix. When  #
# the workflow is run in Predict mode, the model is loaded,    #
# predictions are made, they are un-transformed using the      #
# trained scaler from the training run, and they are written   #
# to a filee named "predictions.csv"                           #
# ------------------------------------------------------------ #


import sklearn.ensemble
import sklearn.metrics
import numpy as np
import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Restore the data
        train_target = context.load("train_target")
        test_target = context.load("test_target")
        train_descriptors = context.load("train_descriptors")
        test_descriptors = context.load("test_descriptors")

        # Flatten the targets
        train_target = train_target.flatten()
        test_target = test_target.flatten()

        # Initialize the Model
        model = sklearn.ensemble.RandomForestClassifier(
            n_estimators=100,
            criterion="gini",
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0.0,
            max_features="auto",
            max_leaf_nodes=None,
            min_impurity_decrease=0.0,
            bootstrap=True,
            oob_score=False,
            verbose=0,
            class_weight=None,
            ccp_alpha=0.0,
            max_samples=None,
        )

        # Train the model and save
        model.fit(train_descriptors, train_target)
        context.save(model, "random_forest")
        train_predictions = model.predict(train_descriptors)
        test_predictions = model.predict(test_descriptors)

        # Save the probabilities of the model
        test_probabilities = model.predict_proba(test_descriptors)
        context.save(test_probabilities, "test_probabilities")

        # Print some information to the screen for the regression problem
        confusion_matrix = sklearn.metrics.confusion_matrix(test_target, test_predictions)
        print("Confusion Matrix:")
        print(confusion_matrix)
        context.save(confusion_matrix, "confusion_matrix")

        context.save(train_predictions, "train_predictions")
        context.save(test_predictions, "test_predictions")

    # Predict
    else:
        # Restore data
        descriptors = context.load("descriptors")

        # Restore model
        model = context.load("random_forest")

        # Make some predictions
        predictions = model.predict(descriptors)

        # Transform predictions back to their original labels
        label_encoder: sklearn.preprocessing.LabelEncoder = context.load("label_encoder")
        predictions = label_encoder.inverse_transform(predictions)

        # Save the predictions to file
        np.savetxt("predictions.csv", predictions, header="prediction", comments="", fmt="%s")
