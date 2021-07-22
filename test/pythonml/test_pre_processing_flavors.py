#!/usr/bin/env python
import importlib
import os
import shutil
import unittest
from parameterized import parameterized
import pandas
import numpy as np
from unittest_baseclass import BaseUnitTest


def load_test_train_targets_and_descriptors():
    """
    Loads a set of commonly used pickle files from an updated location in the context object
    """
    # import and roload settings to update the context object's path dir
    import settings
    importlib.reload(settings)
    train_target = settings.context.load("train_target")
    train_descriptors = settings.context.load("train_descriptors")
    test_target = settings.context.load("test_target")
    test_descriptors = settings.context.load("test_descriptors")
    return train_target, train_descriptors, test_target, test_descriptors


class TestPreProcessingScalerFlavors(BaseUnitTest):
    """
    This class performs unittests for the pre_processing scaler flavors.
    We may only check regression data here, and assume it would work for the other data categories.
    """

    def assert_min_max_pass_condition(self, data):
        for col in data.T:
            self.assertAlmostEqual(1.0, np.amax(col))
            self.assertAlmostEqual(0.0, np.amin(col))

    def assert_standard_scaler_pass_condition(self, data):
        column_means = data.mean(axis=0)
        column_standard_deviations = data.std(axis=0)
        for column_mean in column_means:
            self.assertAlmostEqual(0.0, column_mean)
        for column_standard_deviation in column_standard_deviations:
            self.assertAlmostEqual(1.0, column_standard_deviation)

    def run_scaler_flavor_test(self, category, flavor):
        self.set_pickle_fixtures_path_in_context_object(category, 'unscaled_data')
        shutil.copy(os.path.join(self.asset_path, flavor), flavor)
        os.system('python ' + flavor)
        train_target, train_descriptors, test_target, test_descriptors = load_test_train_targets_and_descriptors()
        # Check the pass conditions for each data loaded
        for data in [train_target, train_descriptors]:
            if 'min_max_scaler' in flavor:
                self.assert_min_max_pass_condition(data)
            elif 'standardization' in flavor:
                self.assert_standard_scaler_pass_condition(data)

    params = [
        ['regression', "pyml:pre_processing:min_max_scaler:sklearn.pyi"],
        ['regression', "pyml:pre_processing:standardization:sklearn.pyi"],
    ]
    @parameterized.expand(params)
    def test_flavor(self, category, flavor):
        self.custom_setup(category)
        self.run_scaler_flavor_test(category, flavor)


class TestPreProcessingRemoveData(BaseUnitTest):
    """
    This class performs unittests for the pre_processing dropper flavors.
    """

    def assert_remove_duplicates_pass_condition(self, data):
        data = pandas.DataFrame(data)
        self.assertFalse(data.duplicated().any())

    def assert_remove_missing_pass_condition(self, data):
        data = pandas.DataFrame(data)
        self.assertFalse(data.isnull().values.any())

    def assert_droppers_pass_conditions(self, data, flavor):
        if 'remove_missing' in flavor:
            self.assert_remove_missing_pass_condition(data)
        elif 'remove_duplicates' in flavor:
            self.assert_remove_duplicates_pass_condition(data)

    params = [
        ['regression', "pyml:pre_processing:remove_duplicates:pandas.pyi"],
        ['regression', "pyml:pre_processing:remove_missing:pandas.pyi"]
    ]
    @parameterized.expand(params)
    def test_flavor(self, category, flavor):

        self.custom_setup(category)

        import settings
        data = pandas.read_csv(settings.datafile)

        # add in some np.nan to the data
        if 'remove_missing' in flavor:
            data.loc[0, 'x1'] = np.nan
            data.loc[1, 'target'] = np.nan

        # duplicate the last row
        elif 'remove_duplicates' in flavor:
            data = data.append(data.tail(1), ignore_index=True)

        # From the fake data, get the target col
        data_target = data.iloc[:, -1]
        data_descriptors = data.iloc[:, :-1]

        with settings.context as context:
            # save fake_data as a pickle in .job_context using context
            context.save(data_target, 'train_target')
            context.save(data_descriptors, 'train_descriptors')
            context.save(data_target, 'test_target')
            context.save(data_descriptors, 'test_descriptors')

        # copy flavor file then run it for training
        shutil.copy(os.path.join(self.asset_path, flavor), flavor)
        os.system('python ' + flavor)

        # Load the (hopefully) modified data in .job_context. We need to reload settings to see whats in .job_context
        # after running the model, here
        train_target, train_descriptors, test_target, test_descriptors = load_test_train_targets_and_descriptors()

        # Check the pass conditions for each data loaded
        for data in [train_target, train_descriptors, test_target, test_descriptors]:
            self.assert_droppers_pass_conditions(data, flavor)


if __name__ == '__main__':
    unittest.main()
