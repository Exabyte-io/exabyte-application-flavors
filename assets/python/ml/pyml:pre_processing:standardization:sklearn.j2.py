# ----------------------------------------------------------------- #
#                                                                   #
#   Sklearn Standard Scaler workflow unit                           #
#                                                                   #
#   This workflow unit scales the data such that it a mean of 0 and #
#   a variance of 1. It then saves the data for use further down    #
#   the road in the workflow, for use in un-transforming the data.  #
#                                                                   #
#   It is important that new predictions are made by scaling the    #
#   new inputs using the mean and variance of the original training #
#   set. As a result, the scaler gets saved in the Training phase.  #
#                                                                   #
#   During a predict workflow, the scaler is loaded, and the        #
#   new examples are scaled using the stored scaler.                #
# ----------------------------------------------------------------- #


import sklearn.preprocessing

import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        # Restore data
        descriptors = context.load("descriptors")
        target = context.load("target")

        # Initialize the scalers
        target_scaler = sklearn.preprocessing.StandardScaler()
        descriptor_scaler = sklearn.preprocessing.StandardScaler()

        # Scale the data
        target_scaler.fit_transform(target)
        descriptor_scaler.fit_transform(descriptors)

        # Save the target and predict scaler (for future predictions)
        context.save(target_scaler, "target_scaler")
        context.save(descriptor_scaler, "descriptor_scaler")

        # Store the data
        context.save(target, "target")
        context.save(descriptors, "descriptors")

    # Predict
    else:
        # Restore data
        descriptors = context.load("descriptors")

        # Get the scaler
        descriptor_scaler = context.load("descriptor_scaler")

        # Scale the data
        descriptors = descriptor_scaler.transform(descriptors)

        # Store the data
        context.save(descriptors, "descriptors")
