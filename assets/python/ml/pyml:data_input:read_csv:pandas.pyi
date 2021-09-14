# ----------------------------------------------------------------- #
#                                                                   #
#   Workflow Unit to read in data for the ML workflow.              #
#                                                                   #
#   Also showcased here is the concept of branching based on        #
#   whether the workflow is in "train" or "predict" mode.           #
#                                                                   #
#   If the workflow is in "training" mode, it will read in the data #
#   before converting it to a Numpy array and save it for use       #
#   later. During training, we already have values for the output,  #
#   and this gets saved to "target."                                #
#                                                                   #
#   Finally, whether the workflow is in training or predict mode,   #
#   it will always read in a set of descriptors from a datafile     #
#   defined in settings.py                                          #
# ----------------------------------------------------------------- #


import pandas
import sklearn.preprocessing
import settings

with settings.context as context:
    data = pandas.read_csv(settings.datafile)

    # Train
    # By default, we don't do train/test splitting: the train and test represent the same dataset at first.
    # Other units (such as a train/test splitter) down the line can adjust this as-needed.
    if settings.is_workflow_running_to_train:

        # Handle the case where we are clustering
        if settings.is_clustering:
            target = data.to_numpy()[:, 0]  # Just get the first column, it's not going to get used anyway
        else:
            target = data.pop(settings.target_column_name).to_numpy()

        # Handle the case where we are classifying. In this case, we must convert any labels provided to be categorical.
        # Specifically, labels are encoded with values between 0 and (N_Classes - 1)
        if settings.is_classification:
            label_encoder = sklearn.preprocessing.LabelEncoder()
            target = label_encoder.fit_transform(target)
            context.save(label_encoder, "label_encoder")

        target = target.reshape(-1, 1)  # Reshape array from a row vector into a column vector

        context.save(target, "train_target")
        context.save(target, "test_target")

        descriptors = data.to_numpy()

        context.save(descriptors, "train_descriptors")
        context.save(descriptors, "test_descriptors")

    else:
        descriptors = data.to_numpy()
        context.save(descriptors, "descriptors")
