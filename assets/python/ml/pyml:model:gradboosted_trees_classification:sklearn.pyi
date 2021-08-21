# ----------------------------------------------------------------- #
#                                                                   #
#   Workflow unit for a gradient boosted classification model with  #
#   Scikit-Learn. Parameters derived from sklearn's defaults.       #
#                                                                   #
#   When then workflow is in Training mode, the model is trained    #
#   and then it is saved, along with the confusion matrix.          #
#                                                                   #
#   When the workflow is run in Predict mode, the model   is        #
#   loaded, predictions are made, they are un-transformed using     #
#   the trained scaler from the training run, and they are          #
#   written to a filed named "predictions.csv"                      #
# ----------------------------------------------------------------- #

import sklearn.ensemble
import sklearn.metrics
import numpy as np
import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Restore the data
        train_target = context.load("train_target")
        train_descriptors = context.load("train_descriptors")
        test_target = context.load("test_target")
        test_descriptors = context.load("test_descriptors")

        # Flatten the targets
        train_target = train_target.flatten()
        test_target = test_target.flatten()

        # Initialize the model
        model = sklearn.ensemble.GradientBoostingClassifier(loss='deviance',
                                                            learning_rate=0.1,
                                                            n_estimators=100,
                                                            subsample=1.0,
                                                            criterion='friedman_mse',
                                                            min_samples_split=2,
                                                            min_samples_leaf=1,
                                                            min_weight_fraction_leaf=0.0,
                                                            max_depth=3,
                                                            min_impurity_decrease=0.0,
                                                            min_impurity_split=None,
                                                            init=None,
                                                            random_state=None,
                                                            max_features=None,
                                                            verbose=0,
                                                            max_leaf_nodes=None,
                                                            warm_start=False,
                                                            validation_fraction=0.1,
                                                            n_iter_no_change=None,
                                                            tol=0.0001,
                                                            ccp_alpha=0.0)

        # Train the model and save
        model.fit(train_descriptors, train_target)
        context.save(model, "gradboosted_trees_classification")
        train_predictions = model.predict(train_descriptors)
        test_predictions = model.predict(test_descriptors)

        # Save the probabilities of the model

        test_probabilities = model.predict_proba(test_descriptors)
        context.save(test_probabilities, "test_probabilities")

        # Print some information to the screen for the regression problem
        confusion_matrix = sklearn.metrics.confusion_matrix(test_target,
                                                            test_predictions)
        print("Confusion Matrix:")
        print(confusion_matrix)
        context.save(confusion_matrix, "confusion_matrix")

        # Ensure predictions have the same shape as the saved target
        train_predictions = train_predictions.reshape(-1, 1)
        test_predictions = test_predictions.reshape(-1, 1)
        context.save(train_predictions, "train_predictions")
        context.save(test_predictions, "test_predictions")

    # Predict
    else:
        # Restore data
        descriptors = context.load("descriptors")

        # Restore model
        model = context.load("gradboosted_trees_classification")

        # Make some predictions
        predictions = model.predict(descriptors)

        # Transform predictions back to their original labels
        label_encoder: sklearn.preprocessing.LabelEncoder = context.load("label_encoder")
        predictions = label_encoder.inverse_transform(predictions)

        # Save the predictions to file
        np.savetxt("predictions.csv", predictions, header="prediction", comments="", fmt="%s")
