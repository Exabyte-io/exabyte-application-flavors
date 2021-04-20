# ------------------------------------------------------------ #
# Workflow unit for k-means clustering.                        #
#                                                              #
# In k-means clustering, the labels are not provided ahead of  #
# time. Instead, one supplies the number of groups the         #
# algorithm should split the dataset into. Here, we set our    #
# own default of 4 groups (fewer than sklearn's default of 8). #
# Otherwise, the default parameters of the clustering method   #
# are the same as in sklearn.                                  #
# ------------------------------------------------------------ #


import sklearn.cluster
import sklearn.metrics
import numpy as np
import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Restore the data
        train_descriptors = context.load("train_descriptors")
        test_descriptors = context.load("test_descriptors")

        # Initialize the Model
        model = sklearn.cluster.KMeans(
            n_clusters=4,
            init="k-means++",
            n_init=10,
            max_iter=300,
            tol=0.0001,
            copy_x=True,
            algorithm="auto",
            verbose=0,
        )

        # Train the model and save
        model.fit(train_descriptors)
        context.save(model, "k_means")
        train_labels = model.predict(train_descriptors)
        test_labels = model.predict(test_descriptors)

        context.save(train_labels, "train_labels")
        context.save(test_labels, "test_labels")

    # Predict
    else:
        # Restore data
        descriptors = context.load("descriptors")

        # Restore model
        model = context.load("k_means")

        # Make some predictions
        predictions = model.predict(descriptors)

        # Save the predictions to file
        np.savetxt("predictions.csv", predictions, header="prediction", comments="", fmt="%s")
