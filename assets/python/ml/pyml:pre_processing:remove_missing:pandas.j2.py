# ----------------------------------------------------------------- #
#                                                                   #
#   Pandas Remove Missing Workflow Unit                             #
#                                                                   #
#   This workflow unit allows missing rows and/or columns to be     #
#   dropped from the dataset by configuring the `to_drop`           #
#   parameter.                                                      #
#                                                                   #
#   Valid values for `to_drop`:                                     #
#   - "rows": rows with missing values will be removed              #
#   - "columns": columns with missing values will be removed        #
#   - "both": rows and columns with missing values will be removed  #
#                                                                   #
# ----------------------------------------------------------------- #


import pandas
import settings

# `to_drop` can either be "rows" or "columns"
# If it is set to "rows" (by default), then all rows with missing values will be dropped.
# If it is set to "columns", then all columns with missing values will be dropped.
# If it is set to "both", then all rows and columns with missing values will be dropped.
to_drop = "rows"


with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Restore the data
        train_target = context.load("train_target")
        train_descriptors = context.load("train_descriptors")
        test_target = context.load("test_target")
        test_descriptors = context.load("test_descriptors")

        # Drop missing from the training set
        df = pandas.DataFrame(train_target, columns=["target"])
        df = df.join(pandas.DataFrame(train_descriptors))

        directions = {
            "rows": ("index",),
            "columns": ("columns",),
            "both": ("index", "columns"),
        }[to_drop]
        for direction in directions:
            df = df.dropna(direction)

        train_target = df.pop("target").to_numpy()
        train_target = train_target.reshape(-1, 1)
        train_descriptors = df.to_numpy()

        # Drop missing from the testing set
        df = pandas.DataFrame(test_target, columns=["target"])
        df = df.join(pandas.DataFrame(test_descriptors))
        df = df.dropna()
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
