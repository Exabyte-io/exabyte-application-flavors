import unittest
import os, shutil, sys
import re
import subprocess
import functools

settings_file_location = "fixtures/settings.py"
training_data_location = "fixtures/data_to_train_with.csv"
predict_data_location = "fixtures/data_to_predict_with.csv"

# Sort out some abbreviations for where things are
# todo: Might refactor this into a dataclass for better error checking / code completion
prefix = "../../assets/python/ml/pyml:"
names_table = {
    "IO_csv": "data_input:read_csv:pandas",
    "IO_tts": "data_input:train_test_split:pandas",
    "PRE_mm": "pre_processing:min_max_scaler:sklearn",
    "PRE_rd": "pre_processing:remove_duplicates:pandas",
    "PRE_rm": "pre_processing:remove_missing:pandas",
    "PRE_st": "pre_processing:standardization:sklearn",
    "REG_abt": "model:adaboosted_trees_regression:sklearn",
    "REG_btr": "model:bagged_trees_regression:sklearn",
    "REG_gbt": "model:gradboosted_trees_regression:sklearn",
    "REG_krr": "model:kernel_ridge_regression:sklearn",
    "REG_lasso": "model:lasso_regression:sklearn",
    "REG_mlp": "model:multilayer_perceptron:sklearn",
    "REG_rf": "model:random_forest_regression:sklearn",
    "REG_rr": "model:ridge_regression:sklearn",
    "POS_pp": "post_processing:parity_plot:matplotlib",
}
suffix = ".j2.py"


class TestWorkflowScripts(unittest.TestCase):
    def setUp(self) -> None:
        shutil.copy(settings_file_location, "settings.py")
        shutil.copy(training_data_location, "data_to_train_with.csv")
        shutil.copy(predict_data_location, "data_to_predict_with.csv")

    def tearDown(self) -> None:
        files_to_remove = (".job_context",
                           "my_parity_plot.png",
                           "predictions.csv",
                           "settings.py",
                           "data_to_train_with.csv",
                           "data_to_predict_with.csv")
        for file in os.listdir():
            if (file in files_to_remove) or file.endswith(suffix):
                try:
                    os.remove(file)
                except (IsADirectoryError, PermissionError):
                    shutil.rmtree(file)
                except FileNotFoundError:
                    pass

    def simulate_workflow(self, in_test):
        to_run = []
        for to_copy in in_test:
            source = prefix + names_table[to_copy] + suffix
            destination = names_table[to_copy] + suffix
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

    def run_test(self, in_test):
        # print("====Training Phase")
        self.simulate_workflow(in_test)
        if "POS_pp" in in_test:
            self.assertTrue(os.path.exists("my_parity_plot.png"))
        # print("===Setting to Predict Mode")
        self.set_to_training_phase()
        # print("====Prediction Phase")
        self.simulate_workflow(in_test)
        self.assertTrue(os.path.exists("predictions.csv"))

    def test_io_minMax_ridge_pp(self):
        in_test = (
            "IO_csv",
            "PRE_mm",
            "REG_rr",
            "POS_pp"
        )
        self.run_test(in_test)

    def test_io_minMax_removeDupes_randomForest_pp(self):
        in_test = (
            "IO_csv",
            "PRE_mm",
            "PRE_rd",
            "REG_rf",
            "POS_pp"
        )
        self.run_test(in_test)

    def test_io_minMax_removeMissing_MLP_pp(self):
        in_test = (
            "IO_csv",
            "PRE_mm",
            "PRE_rm",
            "REG_mlp",
            "POS_pp"
        )
        self.run_test(in_test)

    def test_io_standScale_LASSO_pp(self):
        in_test = (
            "IO_csv",
            "PRE_st",
            "REG_lasso",
            "POS_pp"
        )
        self.run_test(in_test)

    def test_io_standScale_krr_pp(self):
        in_test = (
            "IO_csv",
            "PRE_st",
            "REG_krr",
            "POS_pp"
        )
        self.run_test(in_test)

    def test_io_standScale_GBT_pp(self):
        in_test = (
            "IO_csv",
            "PRE_st",
            "REG_gbt",
            "POS_pp"
        )
        self.run_test(in_test)

    def test_io_minMax_BTR_pp(self):
        in_test = (
            "IO_csv",
            "PRE_mm",
            "REG_btr",
            "POS_pp"
        )
        self.run_test(in_test)

    def test_io_minMax_ABT_pp(self):
        in_test = (
            "IO_csv",
            "PRE_mm",
            "REG_abt",
            "POS_pp"
        )
        self.run_test(in_test)
