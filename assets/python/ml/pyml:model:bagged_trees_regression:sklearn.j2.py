# ----------------------------------------------------------------- #
#                                                                   #
#   Workflow unit for a bagged trees regression model with          #
#   Scikit-Learn. Parameters for the estimator and ensemble         #
#   are derived from sklearn defaults.                              #
#                                                                   #
#   When then workflow is in Training mode, the model is trained    #
#   and then it is saved, along with the RMSE and some              #
#   predictions made using the training data (e.g. for use in a     #
#   parity plot or calculation of other error metrics).             #
#                                                                   #
#   When the workflow is run in Predict mode, the model   is        #
#   loaded, predictions are made, they are un-transformed using     #
#   the trained scaler from the training run, and they are          #
#   written to a filed named "predictions.csv"                      #
# ----------------------------------------------------------------- #

import sklearn.ensemble
import sklearn.tree
import sklearn.metrics
import numpy as np
import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Restore data
        descriptors = context.load("descriptors")
        target = context.load("target")
        target = target.flatten()

        # Initialize the base regressor
        base_estimator = sklearn.tree.DecisionTreeRegressor(criterion="mse",
                                                            splitter="best",
                                                            max_depth="None",
                                                            min_samples_split=2,
                                                            min_samples_leaf=1,
                                                            min_weight_fraction_leaf=0.0,
                                                            max_features=None,
                                                            max_leaf_nodes=None,
                                                            min_impurity_decrease=0.0,
                                                            ccp_alpha=0.0)
        # Initialize
        model = sklearn.ensemble.BaggingRegressor(base_estimator=base_estimator,
                                                  n_estimators=10,
                                                  max_samples=1.0,
                                                  max_features=1.0,
                                                  bootstrap=True,
                                                  bootstreap_features=False,
                                                  oob_score=False,
                                                  verbose=0)

        # Train themodel and save
        model.fit(descriptors, target)
        context.save(model, "random_forest_regression")
        predictions = model.predict(descriptors)

        # Scale predictions so they have the same shape as the saved target
        predictions = predictions.reshape(-1, 1)
        context.save(predictions, "predictions")

        # Scale for RMSE calc
        target_scaler = context.load("target_scaler")
        # Unflatten the target
        target = target.reshape(-1, 1)
        y_true = target_scaler.inverse_transform(target)
        y_pred = target_scaler.inverse_transform(predictions)

        # RMSE
        mse = sklearn.metrics.mean_squared_error(y_true=target_scaler.inverse_transform(target),
                                                 y_pred=target_scaler.inverse_transform(predictions))
        rmse = np.sqrt(mse)
        print(f"RMSE = {rmse}")
        context.save(rmse, "RMSE")

    # Predict
    else:
        # Restore data
        descriptors = context.load("descriptors")

        # Restore model
        model = context.load("random_forest_regression")

        # Make some predictions and unscale
        predictions = model.predict(descriptors)
        predictions = predictions.reshape(-1, 1)
        target_scaler = context.load("target_scaler")

        predictions = target_scaler.inverse_transform(predictions)

        # Save the predictions to file
        np.savetxt("predictions.csv", predictions, header="prediction", comments="")
