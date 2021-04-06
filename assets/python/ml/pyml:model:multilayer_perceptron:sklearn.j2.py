# ----------------------------------------------------------------- #
#                                                                   #
#   Workflow unit to train a simple feedforward neural network      #
#   model on a regression problem using Scikit-Learn.               #
#                                                                   #
#   In this template, we use the default values for                 #
#   hidden_layer_sizes, activation, solver, and learning rate.      #
#   Other parameters are available (consult the sklearn docs), but  #
#   in this case, we only include those relevant to the Adam        #
#   optimizer.                                                      #
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
        target = target.flatten()

        # Initialize the NN model
        model = sklearn.neural_network.MLPRegressor(hidden_layer_sizes=(100,),
                                                    activation="relu",
                                                    solver="adam",
                                                    learning_rate_init=0.001,
                                                    max_iter=200,
                                                    shuffle=True,
                                                    random_state=True,
                                                    tol=1e-4,
                                                    verbose=False,
                                                    early_stopping=False,
                                                    validation_fraction=0.1,
                                                    beta_1=0.9,
                                                    beta_2=0.999,
                                                    epsilon=1e-8,
                                                    n_iter_no_change=10)

        # Train the NN model and save
        model.fit(descriptors, target)
        context.save(model, "sklearn_mlp")
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
        model = context.load("sklearn_mlp")

        # Make some predictions and unscale
        predictions = model.predict(descriptors)
        predictions = predictions.reshape(-1, 1)
        target_scaler = context.load("target_scaler")

        predictions = target_scaler.inverse_transform(predictions)

        # Save the predictions to file
        np.savetxt("predictions.csv", predictions, header="prediction", comments="")
