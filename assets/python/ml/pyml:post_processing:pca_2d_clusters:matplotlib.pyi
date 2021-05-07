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
        xlabel = "Principle Component 1"
        ylabel = "Principle Component 2"

        # Determine the labels we're going to be using, and generate their colors
        labels = set(train_labels)
        colors = {}
        for count, label in enumerate(labels):
            cm = matplotlib.cm.get_cmap('jet', len(labels))
            color = cm(count / len(labels))
            colors[label] = color
        train_colors = [colors[label] for label in train_labels]
        test_colors = [colors[label] for label in test_labels]

        # Train / Test Split Visualization
        plt.title("Train Test Split Visualization")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.scatter(train_descriptors[:, 0], train_descriptors[:, 1], c="#33548c", marker="o", label="Training Set")
        plt.scatter(test_descriptors[:, 0], test_descriptors[:, 1], c="#F0B332", marker="o", label="Testing Set")
        xmin, xmax, ymin, ymax = plt.axis()
        plt.legend()
        plt.tight_layout()
        plt.savefig("train_test_split.png", dpi=600)
        plt.close()

        def clusters_legend(cluster_colors):
            """
            Helper function that creates a legend, given the coloration by clusters.
            Args:
                cluster_colors: A dictionary of the form {cluster_number : color_value}

            Returns:
                None; just creates the legend and puts it on the plot
            """
            legend_symbols = []
            for group, color in cluster_colors.items():
                label = f"Cluster {group}"
                legend_symbols.append(matplotlib.lines.Line2D([], [], color=color, marker="o",
                                                              linewidth=0, label=label))
                plt.legend(handles=legend_symbols)

        # Training Set Clusters
        plt.title("Training Set Clusters")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        plt.scatter(train_descriptors[:, 0], train_descriptors[:, 1], c=train_colors)
        clusters_legend(colors)
        plt.tight_layout()
        plt.savefig("train_clusters.png", dpi=600)
        plt.close()

        # Testing Set Clusters
        plt.title("Testing Set Clusters")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        plt.scatter(test_descriptors[:, 0], test_descriptors[:, 1], c=test_colors)
        clusters_legend(colors)
        plt.tight_layout()
        plt.savefig("test_clusters.png", dpi=600)
        plt.close()


    # Predict
    else:
        # It might not make as much sense to draw a plot when predicting...
        pass
