# ----------------------------------------------------------------- #
#                                                                   #
#   Workflow Unit to perform a train/test split                     #
#                                                                   #
# ----------------------------------------------------------------- #

import sklearn.model_selection
import numpy as np
import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Load training data
        train_target = context.load("train_target")
        train_descriptors = context.load("train_descriptors")

        # Combine datasets to facilitate train/test split

        # Do train/test split
        # percent_held_as_test is the amount of the dataset held out as the testing set. If it is set to 0.2,
        # then 20% of the dataset is held out as a testing set. The remaining 80% is the training set.
        percent_held_as_test = 0.2
        train_descriptors, test_descriptors, train_target, test_target = sklearn.model_selection.train_test_split(
            train_descriptors, train_target, test_size=percent_held_as_test)

        # Set the flag for using a train/test split
        context.save(True, "is_using_train_test_split")

        # Save training data
        context.save(train_target, "train_target")
        context.save(train_descriptors, "train_descriptors")
        context.save(test_target, "test_target")
        context.save(test_descriptors, "test_descriptors")

    # Predict
    else:
        pass
