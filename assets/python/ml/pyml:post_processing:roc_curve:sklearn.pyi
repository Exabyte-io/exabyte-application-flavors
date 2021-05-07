# ----------------------------------------------------------------- #
#                                                                   #
#   ROC Curve Generator                                             #
#                                                                   #
#   Computes and displays the Receiver Operating Characteristic     #
#   (ROC) curve. This is restricted to binary classification tasks. #
#                                                                   #
# ----------------------------------------------------------------- #


import matplotlib.pyplot as plt
import matplotlib.collections
import sklearn.metrics
import numpy as np
import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Restore the data
        test_target = context.load("test_target").flatten()
        # Slice the first column because Sklearn's ROC curve prefers probabilities for the positive class
        test_probabilities = context.load("test_probabilities")[:, 1]

        # Exit if there's more than one label in the predictions
        if len(set(test_target)) > 2:
            exit()

        # ROC curve function in sklearn prefers the positive class
        false_positive_rate, true_positive_rate, thresholds = sklearn.metrics.roc_curve(test_target, test_probabilities,
                                                                                        pos_label=1)
        thresholds[0] -= 1  # Sklearn arbitrarily adds 1 to the first threshold
        roc_auc = np.round(sklearn.metrics.auc(false_positive_rate, true_positive_rate), 3)

        # Plot the curve
        fig, ax = plt.subplots()
        points = np.array([false_positive_rate, true_positive_rate]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        norm = plt.Normalize(thresholds.min(), thresholds.max())
        lc = matplotlib.collections.LineCollection(segments, cmap='jet', norm=norm, linewidths=2)
        lc.set_array(thresholds)
        line = ax.add_collection(lc)
        fig.colorbar(line, ax=ax).set_label('Threshold')

        # Padding to ensure we see the line
        ax.margins(0.01)

        plt.title(f"ROC curve, AUC={roc_auc}")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.tight_layout()
        plt.savefig("my_roc_curve.png", dpi=600)

    # Predict
    else:
        # It might not make as much sense to draw a plot when predicting...
        pass
