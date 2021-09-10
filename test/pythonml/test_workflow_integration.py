import unittest
import os, shutil, sys
import re
import subprocess
import functools
import yaml
from parameterized import parameterized, param
from typing import Dict, List, Any, Tuple, Callable
from unittest_baseclass import BaseUnitTest


with open("integration_configuration.yaml", "r") as inp:
    configuration = yaml.safe_load(inp)

unit_shortnames = configuration["unit_shortnames"]

# ToDo: Refactor data clumps below into classes

# Figure out paths
asset_path = configuration["asset_path"]
fixtures_path = configuration["fixtures"]["path"]
settings_filename = configuration["fixtures"]["settings"]


# Get the path to the training data
def get_dataset_filenames(config: Dict[str, str]) -> Tuple[str, str]:
    """
    Given the configuration for a category of unit test (regression, classification, or clustering), extract out the
    filename of the training and predict test file. These correspond to the "training_set_name" and "predict_set_name"
    keys inside of the fixtures variable defined in integration_configuration.yaml. For example, if regression is
    chosen, "regression_training_data.csv" and "regression_predict_data.csv" will be returned.

    Args:
        config (Dict): Configuration extracted from fixtures in integration_configuration.yaml

    Returns:
        The filename of the training and predict set.
    """
    training_set_name = config["training_set_name"]
    predict_set_name = config["predict_set_name"]
    return training_set_name, predict_set_name


regression_training_file, regression_predict_file = get_dataset_filenames(
    configuration["fixtures"]["regression"])
classification_training_file, classification_predict_file = get_dataset_filenames(
    configuration["fixtures"]["classification"])
clustering_training_file, clustering_predict_file = get_dataset_filenames(
    configuration["fixtures"]["clustering"])

# Which files should we remove
files_to_remove = configuration["files_to_remove"]
extensions_to_remove = configuration["extensions_to_remove"]


# Extract the list of tests
def get_test_names_configs(configuration: List[Dict[str, Any]]) -> Tuple[List[List[str]], List[str]]:
    names = [i[0] for i in configuration]
    tests = [i[1]["units_to_run"] for i in configuration]
    return tests, names


all_tests = configuration["tests"]

regression_configs = [i for i in all_tests.items() if i[1]["category"] == "regression"]
tests_regression, names_regression = get_test_names_configs(regression_configs)

classification_configs = [i for i in all_tests.items() if i[1]["category"] == "classification"]
tests_classification, names_classification = get_test_names_configs(classification_configs)

clustering_configs = [i for i in all_tests.items() if i[1]["category"] == "clustering"]
tests_clustering, names_clustering = get_test_names_configs(clustering_configs)


def custom_name_func(test_names: List[str]) -> Callable:
    def inner(testcase_func: Callable, param_num: int, param: param):
        config_name = list(test_names)[int(param_num)]
        return "%s_%s" % (
            testcase_func.__name__,
            parameterized.to_safe_name(config_name),)

    return inner


class BasePythonMLTest(unittest.TestCase):
    """
    Base class for running tests. The general flow of the tests here is:
    1. Setup
    2. Simulate training workfow
    3. Convert training workflow to a predict workflow
    4. Simulate predict workflow
    5. Cleanup

    Attributes:
        category (str): The type of test this is. Used for controlling what type of training and predict set to
                        copy in during the setUp method. Currently "regresion", "classification", and "clustering"
                        are supported.
    """
    category = ""

    def setUp(self) -> None:
        with open(os.path.join(fixtures_path, settings_filename), "r") as inp, open(settings_filename, "w") as outp:
            for line in inp:
                # Users can select the type of problem category in the settings.py file. Normally, it is set to
                # "regression" by default, but to make the regex more convenient, the settings.py file in fixtures
                # has this value set to "PROBLEM_CATEGORY_HERE"
                line = re.sub("PROBLEM_CATEGORY_HERE", self.category, line)
                outp.write(line)

        if self.category == "regression":
            training_file = regression_training_file
            predict_file = regression_predict_file
        elif self.category == "classification":
            training_file = classification_training_file
            predict_file = classification_predict_file
        elif self.category == "clustering":
            training_file = clustering_training_file
            predict_file = clustering_predict_file
        else:
            training_file = predict_file = -1

        shutil.copy(os.path.join(fixtures_path, training_file), "data_to_train_with.csv")
        shutil.copy(os.path.join(fixtures_path, predict_file), "data_to_predict_with.csv")

    def simulate_workflow(self, in_test: List[str]):
        """
        Runs every unit in the workflow sequentially, simulating what Rupy does in production.

        Args:
            in_test (list):  Units in the workflow
        """
        to_run = []
        for to_copy in in_test:
            source = asset_path + unit_shortnames[to_copy]
            destination = unit_shortnames[to_copy]
            to_run.append(destination)
            if to_copy == "IO_ttSplit":
                shutil.copy(os.path.join(fixtures_path, "train_test_split.py"), destination)
            else:
                shutil.copy(source, destination)

            if to_copy == self.plot_unit:
                BaseUnitTest.template_plot_names(unit_shortnames[to_copy], self.plot_names)

        for file in to_run:
            pipes = subprocess.Popen((sys.executable, file), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = pipes.communicate()

            sys.stdout.write(stdout.decode())

            # Sometimes, Matplotlib will write to stderr to state that it's building the font cache.
            # We can ignore that, safely. See https://github.com/ocropus/ocropy/issues/204
            matplotlib_err_string = "Matplotlib is building the font cache; this may take a moment."
            stderr_decoded = stderr.decode().replace(matplotlib_err_string, "").strip()

            self.assertFalse(stderr_decoded, f"\nSTDERR:\n{stderr_decoded}")


    def set_to_predict_phase(self):
        """
        Adjusts settings.py to convert it from training mode to predict mode. In practice, this operation is
        performed by Express when the predict workflow is generated.
        """
        with open("settings.py", "r") as inp:
            lines = inp.readlines()
            # is_workflow_running_to_predct controls whether the workflow is running in "Train" or "Predict" mode,
            # so we change it to "True" to set the workflow to predict mode.
            sub_partial = functools.partial(re.sub, "(?<=is_workflow_running_to_predict\s=\s)False", "True")
            edited_lines = "".join(map(sub_partial, lines))

        with open("settings.py", "w") as outp:
            for line in edited_lines:
                outp.write(line)


    def run_tests(self, units_in_test: List[str]):
        """
        Does the actual running of the tests. Begins by running every unit in the training workflow, then converts
        to a predict workflow. Ends by running every unit in the predict workflow.

        Args:
            units_in_test (list): A list containing the units in the workflow. The names of the units are defined in
                                  integration_configuration.yaml, as the unit_shortnames.
        """
        # Training Phase
        self.simulate_workflow(units_in_test)
        if self.plot_unit in units_in_test:
            for plot_name in self.plot_names:
                self.assertTrue(os.path.exists(plot_name))

        # Reconfigure for predictions
        self.set_to_predict_phase()

        # Predict Phase
        self.simulate_workflow(units_in_test)
        self.assertTrue(os.path.exists("predictions.csv"))

    def tearDown(self) -> None:
        for file in os.listdir():
            if (file in files_to_remove) or any([file.endswith(ext) for ext in extensions_to_remove]):
                try:
                    os.remove(file)
                except (IsADirectoryError, PermissionError):
                    shutil.rmtree(file)
                except FileNotFoundError:
                    pass


class TestRegression(BasePythonMLTest):
    """
    Class to test regression jobs. Any test inside of integration_configuration.yaml with the category of "regression"
    winds up here.
    Currently, we hardcode in the name of the plot that might be generated (regression jobs generate a parity plot), as
    well as the name of the unit that generates it. Here, "POS_plotParity" will generate a file named
    "my_parity_plot.png." If the plot_unit is present and the file name in plot_name is not generated, the test will
    end in failure.
    """
    category = "regression"
    plot_names = ["my_parity_plot.png"]
    plot_unit = "POS_plotParity"

    @parameterized.expand(tests_regression, testcase_func_name=custom_name_func(names_regression),
                          skip_on_empty=True)
    def test_workflows(self, *units_in_test: List[str]):
        """
        Stub method for parameterized tests. Calls the run_tests method of the base testing class with a list of units.

        Args:
            *units_in_test (list): A list of units in the test, with the same names as those defined in
                                   "unit_shortnames" in integration_configuration.yaml. For example, a simulated
                                   workflow of "IO_readCSV" followed by "REG_lasso" would pass in a list as
                                   ["IO_readCSV", "REG_lasso"]

        Notes:
            The tests are parameterized using parameterized.expand. The "tests_regression" variable above contains a
            list of all the groups of units_in_test (this is a list of lists of strings).

            The custom_name_func will give the test a name containing the test name defined in
            integration_configuration.yaml. For example, if the test was named "Reg_ReadCSV_TrainTest_MinMax_MLP_Parity"
            then the resulting test would be named "test_workflows_Reg_ReadCSV_TrainTest_MinMax_MLP_Parity."

        """
        self.run_tests(units_in_test)


class TestClassification(BasePythonMLTest):
    """
    Class to test classification jobs. Any test inside of integration_configuration.yaml with the category of
    "classification" winds up here.
    Currently, we hardcode in the name of the plot that might be generated (classification jobs generate a parity plot),
    as well as the name of the unit that generates it. Here, "POS_plotROC" will generate a file named
    "my_roc_curve.png." If the plot_unit is present and the file name in plot_name is not generated, the test will
    end in failure.
    """
    category = "classification"
    plot_names = ["my_roc_curve.png"]
    plot_unit = "POS_plotROC"

    @parameterized.expand(tests_classification, testcase_func_name=custom_name_func(names_classification),
                          skip_on_empty=True)
    def test_workflows(self, *units_in_test):
        self.run_tests(units_in_test)


class TestClustering(BasePythonMLTest):
    """
    Class to test clustering jobs. Any test inside of integration_configuration.yaml with the category of "clustering"
    winds up here.
    Currently, we hardcode in the name of the plot that might be generated (clustering jobs generate a parity plot), as
    well as the name of the unit that generates it. Here, "POS_plotClust" will generate a file named
    "my_clusters.png." If the plot_unit is present and the file name in plot_name is not generated, the test will
    end in failure.
    """
    category = "clustering"
    plot_names = ['train_test_split.png', 'train_clusters.png', 'test_clusters.png']
    plot_unit = "POS_plotClusters"

    @parameterized.expand(tests_clustering, testcase_func_name=custom_name_func(names_clustering),
                          skip_on_empty=True)
    def test_workflows(self, *units_in_test):
        self.run_tests(units_in_test)
