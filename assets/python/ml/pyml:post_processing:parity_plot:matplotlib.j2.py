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
        # Load data
        targets = context.load("target")
        predictions = context.load("predictions")

        # Un-transform the data
        target_scaler = context.load("target_scaler")
        targets = target_scaler.inverse_transform(targets)
        predictions = target_scaler.inverse_transform(predictions)

        # Plot the data
        plt.scatter(targets, predictions, c="black", label="Results")
        plt.xlabel("Actual Value")
        plt.ylabel("Predicted Value")

        # Scale the plot
        limits = (min(min(targets), min(predictions)),
                  max(max(targets), max(predictions)))
        plt.xlim = (limits[0], limits[1])
        plt.ylim = (limits[0], limits[1])

        # Draw a parity line, as a guide to the eye
        plt.plot((limits[0], limits[1]), (limits[0], limits[1]), c="grey", linestyle="dotted", label="Parity")
        plt.legend()

        # Save the figure
        plt.savefig("my_parity_plot.png", dpi=300)

    # Predict
    else:
        # It might not make as much sense to draw a parity plot when predicting...
        pass
