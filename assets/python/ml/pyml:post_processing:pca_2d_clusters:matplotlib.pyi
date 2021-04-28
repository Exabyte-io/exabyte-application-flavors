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
        legend_symbols = []
        for group, color in colors.items():
            label = f"Cluster {group}"
            legend_symbols.append(matplotlib.lines.Line2D([], [], color=color, marker="o",
                                                          linewidth=0, label=label))

        fig = plt.figure(figsize=(5,10))
        gs = fig.add_gridspec(3)
        ax1, ax2, ax3 = gs.subplots(sharex=True, sharey=True)

        # Train / Test Split Visualization
        ax1.set_title("Train/Test Split")
        ax1.scatter(train_descriptors[:, 0], train_descriptors[:, 1], c="#33548c", marker="o", label="Training Set")
        ax1.scatter(test_descriptors[:, 0], test_descriptors[:, 1], c="#F0B332", marker="o", label="Testing Set")
        ax1.legend()

        # Training Set Clusters
        ax2.set_title("Training Set Clusters")
        ax2.scatter(train_descriptors[:, 0], train_descriptors[:, 1], c=train_colors)
        ax2.legend(handles=legend_symbols)

        #clusters_legend(colors)

        # Testing Set Clusters
        ax3.set_title("Testing Set Clusters")
        ax3.scatter(test_descriptors[:, 0], test_descriptors[:, 1], c=test_colors)
        ax3.legend(handles=legend_symbols)

        #clusters_legend(colors)

        fig.supxlabel(xlabel)
        fig.supylabel(ylabel)
        fig.tight_layout()
        plt.savefig("my_clusters.png", dpi=600)


    # Predict
    else:
        # It might not make as much sense to draw a parity plot when predicting...
        pass
