import unittest
import os, shutil, sys
import re
import subprocess
import functools
import yaml
from parameterized import parameterized

with open("integration_configuration.yaml", "r") as inp:
    configuration, names_table, test_configs = yaml.safe_load_all(inp)

asset_path = configuration["asset_path"]
fixtures_path = configuration["fixtures"]["path"]
settings_filename = configuration["fixtures"]["settings"]
regression_training_set = configuration["fixtures"]["regression_training_set"]
regression_predict_set = configuration["fixtures"]["regression_predict_set"]

files_to_remove = configuration["files_to_remove"]
extensions_to_remove = configuration["extensions_to_remove"]


def custom_name_func(testcase_func, param_num, param):
    config_name = list(test_configs)[int(param_num)]
    return "%s_%s" % (
        testcase_func.__name__,
        parameterized.to_safe_name(config_name),
    )


test_cases = test_configs.values()


class TestWorkflowScripts(unittest.TestCase):
    def setUp(self) -> None:
        shutil.copy(os.path.join(fixtures_path, settings_filename), settings_filename)
        shutil.copy(os.path.join(fixtures_path, regression_training_set), regression_training_set)
        shutil.copy(os.path.join(fixtures_path, regression_predict_set), regression_predict_set)

    def tearDown(self) -> None:
        for file in os.listdir():
            if (file in files_to_remove) or any([file.endswith(ext) for ext in extensions_to_remove]):
                try:
                    os.remove(file)
                except (IsADirectoryError, PermissionError):
                    shutil.rmtree(file)
                except FileNotFoundError:
                    pass

    def simulate_workflow(self, in_test):
        to_run = []
        for to_copy in in_test:
            source = asset_path + names_table[to_copy]
            destination = names_table[to_copy]
            to_run.append(destination)
            shutil.copy(source, destination)

        for file in to_run:
            # print(file)
            pipes = subprocess.Popen((sys.executable, file), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = pipes.communicate()
            self.assertFalse(stderr, f"\nSTDERR:\n{stderr.decode()}")

    def set_to_training_phase(self):
        with open("settings.py", "r") as inp:
            lines = inp.readlines()
            sub_partial = functools.partial(re.sub, "(?<=is_workflow_running_to_predict\s=\s)False", "True")
            edited_lines = "".join(map(sub_partial, lines))
        with open("settings.py", "w") as outp:
            for line in edited_lines:
                outp.write(line)

    @parameterized.expand(test_cases, testcase_func_name=custom_name_func)
    def test_workflows(self, *units_in_test):
        # print("====Training Phase")
        self.simulate_workflow(units_in_test)
        if "POS_pp" in units_in_test:
            self.assertTrue(os.path.exists("my_parity_plot.png"))
        # print("===Setting to Predict Mode")
        self.set_to_training_phase()
        # print("====Prediction Phase")
        self.simulate_workflow(units_in_test)
        self.assertTrue(os.path.exists("predictions.csv"))
