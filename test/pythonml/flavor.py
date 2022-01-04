import os
import operator

import numpy as np
import pandas as pd

from base import BaseTest


class BaseFlavorTest(BaseTest):
    """
    This class performs unit tests for the model flavors
    """
    needs_data = True

    def set_to_predict_phase(self):
        with open(self.tmppath(self.settings_basename), "r") as settings:
            contents = settings.read()
        with open(self.tmppath(self.settings_basename), "w") as settings:
            settings.write(
                contents.replace(
                    "is_workflow_running_to_predict = False",
                    "is_workflow_running_to_predict = True",
                )
            )

    def assert_preprocessing_success(self, operation: str, data: np.ndarray):
        if operation not in [
            "min_max_scaler",
            "standardization",
            "remove_missing",
            "remove_duplicates",
        ]:
            print(f"scaler", operation, "not validated")
            return
        if operation == "min_max_scaler":
            for col in data.T:
                self.assertAlmostEqual(1.0, np.amax(col))
                self.assertAlmostEqual(0.0, np.amin(col))
        if operation == "standardization":
            means = data.mean(axis=0)
            for mean in means:
                self.assertAlmostEqual(0.0, mean)
            stdevs = data.std(axis=0)
            for stdev in stdevs:
                self.assertAlmostEqual(1.0, stdev)
        if operation == "remove_missing":
            df = pd.DataFrame(data)
            self.assertFalse(df.isnull().values.any())
        if operation == "remove_duplicates":
            df = pd.DataFrame(data)
            self.assertFalse(df.duplicated().any())

    def assert_training_success(self):
        settings = self.reload_settings()
        if self.category not in ["regression", "classification"]:
            print(f"category {self.category} not validated")
            return
        if self.category == "regression":
            compare = operator.le
            threshold = 20
            result = "RMSE"
            mutate = None
        else:
            compare = operator.ge
            threshold = 0.6
            result = "confusion_matrix"
            mutate = lambda val: (val.diagonal() / value.sum(axis=0)).all()
        with settings.context as context:
            value = context.load(result)
            if mutate is not None:
                value = mutate(value)
            self.assertTrue(compare(value, threshold))

    def assert_predicting_success(self):
        self.assertTrue(os.path.isfile(self.tmppath("predictions.csv")))

    def assert_postprocessing_success(self, pngs: list):
        for png in pngs:
            self.assertTrue(os.path.isfile(self.tmppath(png)))

    def get_pickle_file_names(self, data_type: str) -> list:
        names = [
            "train_descriptors",
            "test_descriptors",
            "train_target",
            "test_target",
            "descriptors",
            "label_encoder",
        ]
        return {
            "model_data": {
                "regression": [
                    "train_predictions",
                    "test_predictions",
                    "train_target",
                    "test_target",
                    "target_scaler",
                ],
                "classification": [
                    "test_target",
                    "test_probabilities",
                ],
                "clustering": [
                    "train_descriptors",
                    "test_descriptors",
                    "train_labels",
                    "test_labels",
                    "descriptor_scaler",
                ],
            },
            "scaled_data": {
                "regression": [
                    "train_descriptors",
                    "test_descriptors",
                    "train_target",
                    "test_target",
                    "descriptors",
                    "target_scaler",
                    "descriptor_scaler"
                ]
            }
        }.get(data_type, {}).get(self.category, names)

    def set_pickle_fixtures_path_in_context_object(self, data_type: str):
        settings = self.reload_settings()
        with settings.context as context:
            pickle_files = self.get_pickle_file_names(data_type)
            context.context_paths.update(
                {
                    pickle_file: self.relpath(
                        "{}_pkls/{}/{}.pkl".format(
                            self.category, data_type, pickle_file
                        )
                    )
                    for pickle_file in pickle_files
                }
            )

    def parameterized_setup(self, flavor: str):
        if flavor.startswith("pyml:pre_processing:"):
            data_type = "unscaled_data"
            test_modes = ["preprocessing"]
        elif flavor.startswith("pyml:model:"):
            data_type = "scaled_data"
            test_modes = ["training", "predicting"]
        elif flavor.startswith("pyml:post_processing:"):
            data_type = "model_data"
            test_modes = ["postprocessing"]
        # raise an UndefinedError if not recognized
        self.set_pickle_fixtures_path_in_context_object(data_type)
        self.copy_asset(flavor)
        return test_modes

    def perturb_data(self, flavor: str):
        settings = self.reload_settings()
        data = None
        if "remove_missing" in flavor:
            data = pd.read_csv(settings.datafile)
            data.loc[0, "x1"] = np.nan
            data.loc[1, "target"] = np.nan
        elif "remove_duplicates" in flavor:
            data = pd.read_csv(settings.datafile)
            data = data.append(data.tail(1), ignore_index=True)
        if data is not None:
            with settings.context as context:
                context.save(data.iloc[:, -1], "train_target")
                context.save(data.iloc[:, :-1], "train_descriptors")
                context.save(data.iloc[:, -1], "test_target")
                context.save(data.iloc[:, :-1], "test_descriptors")

    def load_train_test_targets_descriptors(self, operation: str):
        settings = self.reload_settings()
        if operation in ["min_max_scaler", "standardization"]:
            return (
                settings.context.load("train_target"),
                settings.context.load("train_descriptors"),
            )
        return (
            settings.context.load("train_target"),
            settings.context.load("train_descriptors"),
            settings.context.load("test_target"),
            settings.context.load("test_descriptors"),
        )

    def do_flavor(self, flavor, mode, kws):
        """
        This function runs each flavor test whether in training or predict mode.

        Args:
            flavor (str): name of the python model flavor file in assets
            mode (str): one of ['training', 'predicting', 'preprocessing', 'postprocessing']
            kws (dict): keyword args to pass to assertion method
        """
        self.perturb_data(flavor)
        self.run_process(flavor)
        assertion = getattr(self, f"assert_{mode}_success")
        if mode == "preprocessing":
            operation = flavor.split(":")[2]
            all_data = self.load_train_test_targets_descriptors(operation)
            for data in all_data:
                kws.update({"data": data, "operation": operation})
                assertion(**kws)
        else:
            assertion(**kws)

    def run_flavor(self, flavor: str, kws = None):
        test_modes = self.parameterized_setup(flavor)
        for mode in test_modes:
            if mode == "predicting":
                self.set_to_predict_phase()
            self.do_flavor(flavor, mode, kws or {})

    def run_workflow(self, test_params):
        for flavor in test_params["flavors"]:
            self.copy_asset(flavor)
            self.run_process(flavor)
        if self.plot_unit in test_params["units_to_run"]:
            self.assert_postprocessing_success([self.plot_name])
        self.assert_training_success()
        self.set_to_predict_phase()
        for flavor in test_params["flavors"]:
            self.run_process(flavor)
        self.assert_predicting_success()
