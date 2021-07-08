# ----------------------------------------------------------------- #
#                                                                   #
#   General settings for PythonML jobs on the Exabyte.io Platform   #
#                                                                   #
#   This file generally shouldn't be modified directly by users.    #
#   The "datafile" and "is_workflow_running_to_predict" variables   #
#   are defined in the head subworkflow, and are templated into     #
#   this file. This helps facilitate the workflow's behavior        #
#   differing whether it is in a "train" or "predict" mode.         #
#                                                                   #
#   Also in this file is the "Context" object, which helps maintain #
#   certain Python objects between workflow units, and between      #
#   predict runs.                                                   #
#                                                                   #
#   Whenever a python object needs to be stored for subsequent runs #
#   (such as in the case of a trained model), context.save() can be #
#   called to save it. The object can then be loaded again by using #
#   context.load().                                                 #
# ----------------------------------------------------------------- #


import pickle, os

# ==================================================
# Variables modified in the Important Settings menu
# ==================================================
# Variables in this section can (and oftentimes need to) be modified by the user in the "Important Settings" tab
# of a workflow.

# Target_column_name is used during training to identify the variable the model is traing to predict.
# For example, consider a CSV containing three columns, "Y", "X1", and "X2". If the goal is to train a model
# that will predict the value of "Y," then target_column_name would be set to "Y"
target_column_name = "{{ mlSettings.target_column_name }}"

# The type of ML problem being performed. Can be either "regression", "classification," or "clustering."
problem_category = "{{ mlSettings.problem_category }}"

# =============================
# Non user-modifiable variables
# =============================
# Variables in this section generally do not need to be modified.

# The problem category, regression or classification or clustering. In regression, the target (predicted) variable
# is continues. In classification, it is categorical. In clustering, there is no target - a set of labels is
# automatically generated.
is_regression = is_classification = is_clustering = False
if problem_category.lower() == "regression":
    is_regression = True
elif problem_category.lower() == "classification":
    is_classification = True
elif problem_category.lower() == "clustering":
    is_clustering = True
else:
    raise ValueError(
        "Variable 'problem_category' must be either 'regression', 'classification', or 'clustering'. Check settings.py")

# The variables "is_workflow_running_to_predict" and "is_workflow_running_to_train" are used to control whether
# the workflow is in a "training" mode or a "prediction" mode. The "IS_WORKFLOW_RUNNING_TO_PREDICT" variable is set by
# an assignment unit in the "Set Up the Job" subworkflow that executes at the start of the job. It is automatically
# changed when the predict workflow is generated, so users should not need to modify this variable.
is_workflow_running_to_predict = {% raw %}{{IS_WORKFLOW_RUNNING_TO_PREDICT}}{% endraw %}
is_workflow_running_to_train = not is_workflow_running_to_predict

# Sets the datafile variable. The "datafile" is the data that will be read in, and will be used by subsequent
# workflow units for either training or prediction, depending on the workflow mode.
if is_workflow_running_to_predict:
    datafile = "{% raw %}{{DATASET_BASENAME}}{% endraw %}"
else:
    datafile = "{% raw %}{{DATASET_BASENAME}}{% endraw %}"

# The "Context" class allows for data to be saved and loaded between units, and between train and predict runs.
# Variables which have been saved using the "Save" method are written to disk, and the predict workflow is automatically
# configured to obtain these files when it starts.
#
# IMPORTANT NOTE: Do *not* adjust the value of "context_dir_pathname" in the Context object. If the value is changed, then
# files will not be correctly copied into the generated predict workflow. This will cause the predict workflow to be
# generated in a broken state, and it will not be able to make any predictions.
class Context(object):
    """
    Saves and loads objects from the disk, useful for preserving data between workflow units

    Attributes:
        context_paths (dict): Dictionary of the format {variable_name: path}, that governs where
                              pickle saves files.

    Methods:
        save: Used to save objects to the context directory
        load: Used to load objects from the context directory
    """

    def __init__(self, context_file_basename="workflow_context_file_mapping"):
        """
        Constructor for Context objects

        Args:
            context_file_basename (str): Name of the file to store context paths in
        """

        # Warning: DO NOT modify the context_dir_pathname variable below
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        context_dir_pathname = "{% raw %}{{ CONTEXT_DIR_RELATIVE_PATH }}{% endraw %}"
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self._context_dir_pathname = context_dir_pathname
        self._context_file = os.path.join(context_dir_pathname, context_file_basename)

        # Make context dir if it does not exist
        if not os.path.exists(context_dir_pathname):
            os.makedirs(context_dir_pathname)

        # Read in the context sources dictionary, if it exists
        if os.path.exists(self._context_file):
            with open(self._context_file, "rb") as file_handle:
                self.context_paths: dict = pickle.load(file_handle)
        else:
            # Items is a dictionary of {varname: path}
            self.context_paths = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._update_context()

    def __contains__(self, item):
        return item in self.context_paths

    def _update_context(self):
        with open(self._context_file, "wb") as file_handle:
            pickle.dump(self.context_paths, file_handle)

    def load(self, name: str):
        """
        Returns a contextd object

        Args:
            name (str): The name in self.context_paths of the object
        """
        path = self.context_paths[name]
        with open(path, "rb") as file_handle:
            obj = pickle.load(file_handle)
        return obj

    def save(self, obj: object, name: str):
        """
        Saves an object to disk using pickle

        Args:
            name (str): Friendly name for the object, used for lookup in load() method
            obj (object): Object to store on disk
        """
        path = os.path.join(self._context_dir_pathname, f"{name}.pkl")
        self.context_paths[name] = path
        with open(path, "wb") as file_handle:
            pickle.dump(obj, file_handle)
        self._update_context()

# Generate a context object, so that the "with settings.context" can be used by other units in this workflow.
context = Context()

is_using_train_test_split = "is_using_train_test_split" in context and (context.load("is_using_train_test_split"))

# Create a Class for a DummyScaler()
class DummyScaler:
    """
    This class is a 'DummyScaler' which trivially acts on data by returning it unchanged.
    """

    def fit(self, X):
        return self

    def transform(self, X):
        return X

    def fit_transform(self, X):
        return X

    def inverse_transform(self, X):
        return X

if 'target_scaler' not in context:
    context.save(DummyScaler(), 'target_scaler')
