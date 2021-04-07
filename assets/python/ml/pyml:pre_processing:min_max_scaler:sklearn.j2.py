# ----------------------------------------------------------------- #
#                                                                   #
#   Sklearn MinMax Scaler workflow unit                             #
#                                                                   #
#   This workflow unit scales the data such that it is on interval  #
#   [0,1]. It then saves the data for use further down              #
#   the road in the workflow, for use in un-transforming the data.  #
#                                                                   #
#   It is important that new predictions are made by scaling the    #
#   new inputs using the min and max of the original training       #
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
        # Restore the data
        train_target = context.load("train_target")
        train_descriptors = context.load("train_descriptors")
        test_target = context.load("test_target")
        test_descriptors = context.load("test_descriptors")

        # Initialize the scalers
        scaler = sklearn.preprocessing.MinMaxScaler
        target_scaler = scaler()
        descriptor_scaler = scaler()

        # Scale the data
        train_target = target_scaler.fit_transform(train_target)
        train_descriptors = descriptor_scaler.fit_transform(train_descriptors)
        test_target = target_scaler.transform(test_target)
        test_descriptors = descriptor_scaler.transform(test_descriptors)

        # Save the target and predict scaler (for future predictions)
        context.save(target_scaler, "target_scaler")
        context.save(descriptor_scaler, "descriptor_scaler")

        # Store the data
        context.save(train_target, "train_target")
        context.save(train_descriptors, "train_descriptors")
        context.save(test_target, "test_target")
        context.save(test_descriptors, "test_descriptors")
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
