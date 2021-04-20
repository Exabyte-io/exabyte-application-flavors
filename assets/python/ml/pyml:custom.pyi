# ----------------------------------------------------------------- #
#                                                                   #
#   Custom workflow unit template for the Exabyte.io platform       #
#                                                                   #
#   This file imports a set of workflow-specific context variables  #
#   from settings.py. It then uses a context manager to save and    #
#   load Python objects. When saved, these objects can then be      #
#   loaded either later in the same workflow, or by subsequent      #
#   predict jobs.                                                   #
#                                                                   #
#   Any pickle-able Python object can be saved using                #
#   settings.context.                                               #
#                                                                   #
# ----------------------------------------------------------------- #


import settings

# The context manager exists to facilitate
# saving and loading objects across Python units within a workflow.

# To load an object, simply do to \`context.load("name-of-the-saved-object")\`
# To save an object, simply do \`context.save("name-for-the-object", object_here)\`
with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        train_target = context.load("train_target")
        train_descriptors = context.load("train_descriptors")
        test_target = context.load("test_target")
        test_descriptors = context.load("test_descriptors")

        # Do some transformations to the data here

        context.save(train_target, "train_target")
        context.save(train_descriptors, "train_descriptors")
        context.save(test_target, "test_target")
        context.save(test_descriptors, "test_descriptors")

    # Predict
    else:
        descriptors = context.load("descriptors")

        # Do some predictions or transformation to the data here
