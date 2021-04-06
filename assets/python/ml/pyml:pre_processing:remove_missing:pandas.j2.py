# ----------------------------------------------------------------- #
#                                                                   #
#   Pandas Remove Duplicates workflow unit                          #
#                                                                   #
#   This workflow unit drops all missing rows, if it is running     #
#   in the "train" mode.                                            #
# ----------------------------------------------------------------- #


import pandas
import settings

with settings.context as context:
    # Train
    if settings.is_workflow_running_to_train:
        target = context.load("target")
        descriptors = context.load("descriptors")

        df = pandas.DataFrame(target, columns=["target"])
        df = df.join(pandas.DataFrame(descriptors))

        df = df.dropna()

        target = df.pop("target").to_numpy()
        target = target.reshape(-1,1)

        descriptors = df.to_numpy()

        context.save(target, "target")
        context.save(descriptors, "descriptors")

    # Predict
    else:
        pass
