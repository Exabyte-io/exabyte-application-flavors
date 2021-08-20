# ----------------------------------------------------------------- #
#                                                                   #
#   Workflow unit for eXtreme Gradient-Boosted trees regression     #
#   with XGBoost's wrapper to Scikit-Learn. Parameters for the      #
#   estimator and ensemble are derived from sklearn defaults.       #
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

import xgboost
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
        model = xgboost.XGBRegressor(booster='gbtree',
                                     verbosity=1,
                                     learning_rate=0.3,
                                     min_split_loss=0,
                                     max_depth=6,
                                     min_child_weight=1,
                                     max_delta_step=0,
                                     colsample_bytree=1,
                                     reg_lambda=1,
                                     reg_alpha=0,
                                     scale_pos_weight=1,
                                     objective='reg:squarederror',
                                     eval_metric='rmse')

        # Train the model and save
        model.fit(train_descriptors, train_target)
        context.save(model, "extreme_gradboosted_tree_regression")
        train_predictions = model.predict(train_descriptors)
        test_predictions = model.predict(test_descriptors)

        # Scale predictions so they have the same shape as the saved target
        train_predictions = train_predictions.reshape(-1, 1)
        test_predictions = test_predictions.reshape(-1, 1)
        context.save(train_predictions, "train_predictions")
        context.save(test_predictions, "test_predictions")

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

    # Predict
    else:
        # Restore data
        descriptors = context.load("descriptors")

        # Restore model
        model = context.load("extreme_gradboosted_tree_regression")

        # Make some predictions and unscale
        predictions = model.predict(descriptors)
        predictions = predictions.reshape(-1, 1)
        target_scaler = context.load("target_scaler")

        predictions = target_scaler.inverse_transform(predictions)

        # Save the predictions to file
        np.savetxt("predictions.csv", predictions, header="prediction", comments="")
