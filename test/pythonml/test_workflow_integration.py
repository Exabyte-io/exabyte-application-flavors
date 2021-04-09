import unittest
import os, shutil, sys
import re
import subprocess
import functools
import yaml
from parameterized import parameterized

with open("integration_configuration.yaml", "r") as inp:
    configuration = yaml.safe_load(inp)

unit_shortnames = configuration["unit_shortnames"]

# ToDo: Refactor data clumps below into classes

# Figure out paths
asset_path = configuration["asset_path"]
fixtures_path = configuration["fixtures"]["path"]
settings_filename = configuration["fixtures"]["settings"]


# Get the path to the training data
def get_dataset_filenames(config):
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
def get_test_names_configs(configuration):
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


def custom_name_func(test_names):
    def inner(testcase_func, param_num, param):
        config_name = list(test_names)[int(param_num)]
        return "%s_%s" % (
            testcase_func.__name__,
            parameterized.to_safe_name(config_name),)

    return inner


class BasePythonMLTest(unittest.TestCase):
    category = ""

    def setUp(self) -> None:
        with open(os.path.join(fixtures_path, settings_filename), "r") as inp, open(settings_filename, "w") as outp:
            for line in inp:
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

    def simulate_workflow(self, in_test):
        to_run = []
        for to_copy in in_test:
            source = asset_path + unit_shortnames[to_copy]
            destination = unit_shortnames[to_copy]
            to_run.append(destination)
            shutil.copy(source, destination)

        for file in to_run:
            pipes = subprocess.Popen((sys.executable, file), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = pipes.communicate()

            sys.stdout.write(stdout.decode())

            self.assertFalse(stderr, f"\nSTDERR:\n{stderr.decode()}")

    def set_to_predict_phase(self):
        with open("settings.py", "r") as inp:
            lines = inp.readlines()
            sub_partial = functools.partial(re.sub, "(?<=is_workflow_running_to_predict\s=\s)False", "True")
            edited_lines = "".join(map(sub_partial, lines))

        with open("settings.py", "w") as outp:
            for line in edited_lines:
                outp.write(line)

    def run_tests(self, units_in_test):

        # Training Phase
        self.simulate_workflow(units_in_test)
        if self.plot_unit in units_in_test:
            self.assertTrue(os.path.exists(self.plot_name))

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
    category = "regression"
    plot_name = "my_parity_plot.png"
    plot_unit = "POS_plotParity"

    @parameterized.expand(tests_regression, testcase_func_name=custom_name_func(names_regression),
                          skip_on_empty=True)
    def test_workflows(self, *units_in_test):
        self.run_tests(units_in_test)


class TestClassification(BasePythonMLTest):
    category = "classification"
    plot_name = "my_roc_curve.png"
    plot_unit = "POS_plotROC"

    @parameterized.expand(tests_classification, testcase_func_name=custom_name_func(names_classification),
                          skip_on_empty=True)
    def test_workflows(self, *units_in_test):
        self.run_tests(units_in_test)


class TestClustering(BasePythonMLTest):
    category = "clustering"
    plot_name = "my_clusters.png"
    plot_unit = "POS_plotClust"

    @parameterized.expand(tests_clustering, testcase_func_name=custom_name_func(names_clustering),
                          skip_on_empty=True)
    def test_workflows(self, *units_in_test):
        self.run_tests(units_in_test)
