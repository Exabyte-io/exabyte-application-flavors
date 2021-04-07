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

import settings

with settings.context as context:
    data = pandas.read_csv(settings.datafile)

    # Train
    # By default, we don't do train/test splitting; in other words, the train/test set are one and the same.
    # Other units (such as a train/test splitter) down the line can adjust this as-needed.
    if settings.is_workflow_running_to_train:
        target = data.pop(settings.target_column_name).to_numpy()
        target = target.reshape(-1, 1)  # Reshape array to be used by sklearn
        descriptors = data.to_numpy()

        context.save(target, "train_target")
        context.save(descriptors, "train_descriptors")
        context.save(target, "test_target")
        context.save(descriptors, "test_descriptors")

    # Predict
    else:
        descriptors = data.to_numpy()
        context.save(descriptors, "descriptors")

