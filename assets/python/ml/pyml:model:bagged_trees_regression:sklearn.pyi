# ------------------------------------------------------------ #
# Workflow unit for a bagged trees regression model with       #
# Scikit-Learn. Parameters for the estimator and ensemble are  #
# derived from Scikit-Learn's Defaults.                        #
#                                                              #
# When then workflow is in Training mode, the model is trained #
# and then it is saved, along with the RMSE and some           #
# predictions made using the training data (e.g. for use in a  #
# parity plot or calculation of other error metrics). When the #
# workflow is run in Predict mode, the model is loaded,        #
# predictions are made, they are un-transformed using the      #
# trained scaler from the training run, and they are written   #
# to a file named "predictions.csv"                            #
# ------------------------------------------------------------ #


import sklearn.ensemble
import sklearn.tree
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

        # Initialize the Base Estimator
        base_estimator = sklearn.tree.DecisionTreeRegressor(
            criterion="mse",
            splitter="best",
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0.0,
            max_features=None,
            max_leaf_nodes=None,
            min_impurity_decrease=0.0,
            ccp_alpha=0.0,
        )

        # Initialize the Model
        model = sklearn.ensemble.BaggingRegressor(
            n_estimators=10,
            max_samples=1.0,
            max_features=1.0,
            bootstrap=True,
            bootstrap_features=False,
            oob_score=False,
            verbose=0,
            base_estimator=base_estimator,
        )

        # Train the model and save
        model.fit(train_descriptors, train_target)
        context.save(model, "bagged_trees")
        train_predictions = model.predict(train_descriptors)
        test_predictions = model.predict(test_descriptors)

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

        context.save(train_predictions, "train_predictions")
        context.save(test_predictions, "test_predictions")

    # Predict
    else:
        # Restore data
        descriptors = context.load("descriptors")

        # Restore model
        model = context.load("bagged_trees")

        # Make some predictions
        predictions = model.predict(descriptors)

        # Save the predictions to file
        np.savetxt("predictions.csv", predictions, header="prediction", comments="", fmt="%s")
