# ----------------------------------------------------------------- #
#                                                                   #
#   Cluster Visualization                                           #
#                                                                   #
#   This unit takes an N-dimensional feature space, and uses        #
#   Principal-component Analysis (PCA) to project into a 2D space   #
#   to facilitate plotting on a scatter plot.                       #
#                                                                   #
#   The 2D space we project into are the first two principal        #
#   components identified in PCA, which are the two vectors with    #
#   the highest variance.                                           #
#                                                                   #
#   Wikipedia Article on PCA:                                       #
#   https://en.wikipedia.org/wiki/Principal_component_analysis      #
#                                                                   #
#   We then plot the labels assigned to the train an test set,      #
#   and color by class.                                             #
#                                                                   #
# ----------------------------------------------------------------- #

import pandas as pd
import matplotlib.cm
import matplotlib.lines
import matplotlib.pyplot as plt
import sklearn.decomposition
import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Restore the data
        train_labels = context.load("train_labels")
        train_descriptors = context.load("train_descriptors")
        test_labels = context.load("test_labels")
        test_descriptors = context.load("test_descriptors")

        # Unscale the descriptors
        descriptor_scaler = context.load("descriptor_scaler")
        train_descriptors = descriptor_scaler.inverse_transform(train_descriptors)
        test_descriptors = descriptor_scaler.inverse_transform(test_descriptors)

        # We need at least 2 dimensions, exit if the dataset is 1D
        if train_descriptors.ndim < 2:
            raise ValueError("The train descriptors do not have enough dimensions to be plot in 2D")

        # The data could be multidimensional. Let's do some PCA to get things into 2 dimensions.
        pca = sklearn.decomposition.PCA(n_components=2)
        train_descriptors = pca.fit_transform(train_descriptors)
        test_descriptors = pca.transform(test_descriptors)

        labels = set(train_labels)
        colors = {}
        for count, label in enumerate(labels):
            cm = matplotlib.cm.get_cmap('Blues', len(labels))
            color = cm(count / len(labels))
            colors[label] = color

        train_colors = [colors[label] for label in train_labels]
        train_marker = "o"
        test_colors = [colors[label] for label in test_labels]
        test_marker = "s"

        # Plot the data
        plt.scatter(train_descriptors[:, 0], train_descriptors[:, 1], c=train_colors, marker=train_marker,
                    edgecolors="black",
                    label="Training Set")
        if settings.is_using_train_test_split:
            plt.scatter(test_descriptors[:, 0], test_descriptors[:, 1], c=test_colors, marker=test_marker,
                        alpha=1, edgecolors="black",
                        label="Testing Set")
        plt.title("Results (Colored by Cluster)")
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")

        # Configure the legend
        train_legend_symbol = matplotlib.lines.Line2D([], [], color='white', marker=train_marker,
                                                      markeredgecolor="black",
                                                      label="Training Set")
        test_legend_symbol = matplotlib.lines.Line2D([], [], color='white', marker=test_marker,
                                                     markeredgecolor="black",
                                                     label="Testing Set")

        plt.legend(handles=[train_legend_symbol, test_legend_symbol])

        # Save the figure
        plt.savefig("my_clusters.png", dpi=600)


    # Predict
    else:
        # It might not make as much sense to draw a parity plot when predicting...
        pass
