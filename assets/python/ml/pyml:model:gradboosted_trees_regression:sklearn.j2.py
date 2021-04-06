# ----------------------------------------------------------------- #
#                                                                   #
#   Workflow unit for gradient-boosted trees regression with        #
#   Scikit-Learn. Parameters for the estimator and ensemble         #
#   are derived from sklearn defaults.                              #
#                                                                   #
#   Note: In the gradient-boosted trees ensemble used, the weak     #
#   learners used as estimators cannot be tuned with the same level #
#   of fidelity allowed in the Adaptive-Boosted Trees ensemble      #
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

        # Initialize the model
        model = sklearn.ensemble.GradientBoostingRegressor(loss="ls",
                                                           learning_rate=0.1,
                                                           n_estimators=100,
                                                           subsample=1.0,
                                                           criterion="friedman_mse",
                                                           min_samples_split=2,
                                                           min_samples_leaf=1,
                                                           min_weight_fraction_leaf=0.0,
                                                           max_depth=3,
                                                           min_impurity_decrease=0.0,
                                                           max_features=None,
                                                           alpha=0.9,
                                                           verbose=0,
                                                           max_leaf_nodes=None,
                                                           validation_fraction=0.1,
                                                           n_iter_no_change=None,
                                                           tol=1e-4,
                                                           ccp_alpha=0.0)

        # Train themodel and save
        model.fit(descriptors, target)
        context.save(model, "gradboosted_tree_regression")
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
        model = context.load("gradboosted_tree_regression")

        # Make some predictions and unscale
        predictions = model.predict(descriptors)
        predictions = predictions.reshape(-1, 1)
        target_scaler = context.load("target_scaler")

        predictions = target_scaler.inverse_transform(predictions)

        # Save the predictions to file
        np.savetxt("predictions.csv", predictions, header="prediction", comments="")
