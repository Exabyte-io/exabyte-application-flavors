# ----------------------------------------------------------------- #
#                                                                   #
#   Workflow Unit to perform a train/test split                     #
#                                                                   #
#   Splits the dataset into a training and testing set. The         #
#   variable `percent_held_as_test` controls how much of the        #
#   input dataset is removed for use as a testing set. By default,  #
#   this unit puts 20% of the dataset into the testing set, and     #
#   places the remaining 80% into the training set.                 #
#                                                                   #
#   Does nothing in the case of predictions.                        #
#                                                                   #
# ----------------------------------------------------------------- #

import sklearn.model_selection
import numpy as np
import settings

# `percent_held_as_test` is the amount of the dataset held out as the testing set. If it is set to 0.2,
# then 20% of the dataset is held out as a testing set. The remaining 80% is the training set.
percent_held_as_test = {{ mlTrainTestSplit.fraction_held_as_test_set }}

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Load training data
        train_target = context.load("train_target")
        train_descriptors = context.load("train_descriptors")

        # Combine datasets to facilitate train/test split

        # Do train/test split
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
