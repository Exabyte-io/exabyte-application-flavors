# ----------------------------------------------------------------- #
#                                                                   #
#   Parity plot generation unit                                     #
#                                                                   #
#   This unit generates a parity plot based on the known values     #
#   in the training data, and the predicted values generated        #
#   using the training data.                                        #
#                                                                   #
#   Because this metric compares predictions versus a ground truth, #
#   it doesn't make sense to generate the plot when a predict       #
#   workflow is being run (because in that case, we generally don't #
#   know the ground truth for the values being predicted). Hence,   #
#   this unit does nothing if the workflow is in "predict" mode.    #
# ----------------------------------------------------------------- #


import matplotlib.pyplot as plt

import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Restore the data
        train_target = context.load("train_target")
        train_predictions = context.load("train_predictions")
        test_target = context.load("test_target")
        test_predictions = context.load("test_predictions")

        # Un-transform the data
        target_scaler = context.load("target_scaler")
        train_target = target_scaler.inverse_transform(train_target)
        train_predictions = target_scaler.inverse_transform(train_predictions)
        test_target = target_scaler.inverse_transform(test_target)
        test_predictions = target_scaler.inverse_transform(test_predictions)

        # Plot the data
        plt.scatter(train_target, train_predictions, c="#203d78", label="Training Set")
        if settings.is_using_train_test_split:
            plt.scatter(test_target, test_predictions, c="#67ac5b", label="Testing Set")
        plt.xlabel("Actual Value")
        plt.ylabel("Predicted Value")

        # Scale the plot
        target_range = (min(min(train_target), min(test_target)),
                        max(max(train_target), max(test_target)))
        predictions_range = (min(min(train_predictions), min(test_predictions)),
                             max(max(train_predictions), max(test_predictions)))

        limits = (min(min(target_range), min(target_range)),
                  max(max(predictions_range), max(predictions_range)))
        plt.xlim = (limits[0], limits[1])
        plt.ylim = (limits[0], limits[1])

        # Draw a parity line, as a guide to the eye
        plt.plot((limits[0], limits[1]), (limits[0], limits[1]), c="black", linestyle="dotted", label="Parity")
        plt.legend()

        # Save the figure
        plt.tight_layout()
        plt.savefig("my_parity_plot.png", dpi=600)

    # Predict
    else:
        # It might not make as much sense to draw a plot when predicting...
        pass
