# ----------------------------------------------------------------- #
#                                                                   #
#   Pandas Remove Duplicates workflow unit                          #
#                                                                   #
#   This workflow unit drops all duplicate rows, if it is running   #
#   in the "train" mode.                                            #
# ----------------------------------------------------------------- #


import pandas
import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Restore the data
        train_target = context.load("train_target")
        train_descriptors = context.load("train_descriptors")
        test_target = context.load("test_target")
        test_descriptors = context.load("test_descriptors")

        # Drop duplicates from the training set
        df = pandas.DataFrame(train_target, columns=["target"])
        df = df.join(pandas.DataFrame(train_descriptors))
        df = df.drop_duplicates()
        train_target = df.pop("target").to_numpy()
        train_target = train_target.reshape(-1, 1)
        train_descriptors = df.to_numpy()

        # Drop duplicates from the testing set
        df = pandas.DataFrame(test_target, columns=["target"])
        df = df.join(pandas.DataFrame(test_descriptors))
        df = df.drop_duplicates()
        test_target = df.pop("target").to_numpy()
        test_target = test_target.reshape(-1, 1)
        test_descriptors = df.to_numpy()

        # Store the data
        context.save(train_target, "train_target")
        context.save(train_descriptors, "train_descriptors")
        context.save(test_target, "test_target")
        context.save(test_descriptors, "test_descriptors")

    # Predict
    else:
        pass
