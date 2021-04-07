# ----------------------------------------------------------------- #
#                                                                   #
#   ROC Curve Generator                                             #
#                                                                   #
#   Computes and displays the Receiver Operating Characteristic     #
#   (ROC) curve. This is restricted to binary classification tasks. #
#                                                                   #
# ----------------------------------------------------------------- #


import matplotlib.pyplot as plt
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
        roc_auc = np.round(sklearn.metrics.auc(false_positive_rate, true_positive_rate), 3)

        # Plot the curve
        plt.plot(false_positive_rate, true_positive_rate, c="#203d78", label=f"ROC Cure, AUC={roc_auc}")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.xlim([0,1])
        plt.ylim([0,1])
        plt.legend()

        plt.savefig("my_roc_curve.png")

    # Predict
    else:
        # It might not make as much sense to draw a parity plot when predicting...
        pass
