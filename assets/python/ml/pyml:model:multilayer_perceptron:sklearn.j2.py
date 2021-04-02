# ----------------------------------------------------------------- #
#                                                                   #
#   Workflow unit to train a simple feedforward neural network      #
#   model on a regression problem using Scikit-Learn.               #
#                                                                   #
#   In this template, we use the default values for                 #
#   hidden_layer_sizes, activation, solver, and learning rate.      #
#                                                                   #
#   When then workflow is in Training mode, the network is trained  #
#   and the model is saved, along with the RMSE and some            #
#   predictions made using the training data (e.g. for use in a     #
#   parity plot or calculation of other error metrics).             #
#                                                                   #
#   When the workflow is run in Predict mode, the network is        #
#   loaded, predictions are made, they are un-transformed using     #
#   the trained scaler from the training run, and they are          #
#   written to a filed named "predictions.csv"                      #
# ----------------------------------------------------------------- #

import sklearn.neural_network
import sklearn.metrics
import numpy as np
import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Restore data
        descriptors = context.load("descriptors")
        target = context.load("target")

        # Transform targets from shape (100,1) to shape (100,); required by sklearn's MLP Regressor
        target = target.ravel()

        # Initialize the NN model
        model = sklearn.neural_network.MLPRegressor(hidden_layer_sizes=(100,),
                                                    activation="relu",
                                                    solver="adam",
                                                    learning_rate="adaptive",
                                                    max_iter=500)

        # Train the NN model and save
        model.fit(descriptors, target)
        context.save(model, "sklearn_mlp")

        # Print RMSE to stdout and save
        predictions = model.predict(descriptors)
        context.save(predictions, "predictions")
        target_scaler = context.load("target_scaler")

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
        model = context.load("sklearn_mlp")

        # Make some predictions and unscale
        predictions = model.predict(descriptors)
        target_scaler = context.load("target_scaler")
        predictions = target_scaler.inverse_transform(predictions)

        # Save the predictions to file
        np.savetxt("predictions.csv", predictions, header="prediction", comments="")
