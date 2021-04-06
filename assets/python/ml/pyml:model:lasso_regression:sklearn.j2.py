# ----------------------------------------------------------------- #
#                                                                   #
#   Workflow unit for a LASSO-regression model with Scikit-Learn    #
#   Model parameters derived from sklearn defaults.                 #
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

import sklearn.linear_model
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
        model = sklearn.linear_model.Lasso(alpha=1.0,
                                           fit_intercept=True,
                                           normalize=False,
                                           precompute=False,
                                           tol=1e-4,
                                           positive=True,
                                           selection="cyclic")

        # Train themodel and save
        model.fit(descriptors, target)
        context.save(model, "lasso_regression")
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
        model = context.load("lasso_regression")

        # Make some predictions and unscale
        predictions = model.predict(descriptors)
        predictions = predictions.reshape(-1, 1)
        target_scaler = context.load("target_scaler")

        predictions = target_scaler.inverse_transform(predictions)

        # Save the predictions to file
        np.savetxt("predictions.csv", predictions, header="prediction", comments="")
