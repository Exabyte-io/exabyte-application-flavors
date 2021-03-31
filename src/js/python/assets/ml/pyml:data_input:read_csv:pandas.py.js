export default `# ----------------------------------------------------------------- #
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

    if settings.is_workflow_running_to_train:
        # If we're training, we have an extra targets column to extract
        target = data.pop(settings.target_column_name).to_numpy()
        target = target.reshape(-1, 1)  # Reshape array to be used by sklearn
        context.save(target, "target")

    # Save descriptors
    descriptors = data.to_numpy()
    context.save(descriptors, "descriptors")
`;

