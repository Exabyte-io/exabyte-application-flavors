#!/usr/bin/env python
import importlib
import os
import re
import shutil
import unittest
import functools
from parameterized import parameterized
import pandas
import numpy as np


class BaseUnitTest(unittest.TestCase):
    """
    Base class for the unit tests.
    It sets up the unit test by getting settings.py from fixtures and editing for the test to be done.
    """

    asset_path = '../../assets/python/ml'
    fixtures_path = 'fixtures'
    settings_filename = 'settings.py'

    def custom_setup(self, category):
        """
        This is a custom setup function

        Args:
            category (str): the category of data we are to use:
                Ex) 'regression', 'classification', 'clustering'
        """

        with open(os.path.join(self.fixtures_path, self.settings_filename), "r") as inp, \
                open(self.settings_filename, "w") as outp:
            for line in inp:
                # Users can select the type of problem category in the settings.py file. Normally, it is set to
                # "regression" by default, but to make the regex more convenient, the settings.py file in fixtures
                # has this value set to "category_HERE"
                line = re.sub("PROBLEM_CATEGORY_HERE", category, line)
                outp.write(line)

        if category == 'regression' or category == 'classification':
            training_file = '{}_training_data.csv'.format(category)
            predict_file = '{}_predict_data.csv'.format(category)
        elif category == 'clustering':
            training_file = predict_file = 'clustering_blobs.csv'
        else:
            training_file = predict_file = -1
        shutil.copy(os.path.join(self.fixtures_path, training_file), "data_to_train_with.csv")
        shutil.copy(os.path.join(self.fixtures_path, predict_file), "data_to_predict_with.csv")

        import settings
        importlib.reload(settings)

    @staticmethod
    def set_to_predict_phase():
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

    @staticmethod
    def get_needed_pickle_file_names(category, data_type):
        """
        This function returns a list of names that are the 'names' of the pickle objects one
        needs to get based on their test conditions

        Args:
            category (str): which category of data is being used. (regression, classification, etc)
            data_type (str): the folder within fixtures/category that is to be used
                ex) unscaled, scaled, or model.
                    - use 'unscaled' if you are testing the min_max scaler
                    - use 'scaled' if testing a model flavor
                    - use 'model' if testing a post processor
        """

        if data_type == 'model' and category == 'regression':
            pickle_file_names = ['train_predictions', 'test_predictions', 'train_target', 'test_target',
                                 'target_scaler']
        elif data_type == 'model' and category == 'classification':
            pickle_file_names = ['test_target', 'test_probabilities']
        elif data_type == 'model' and category == 'clustering':
            pickle_file_names = ['train_descriptors', 'test_descriptors', 'train_labels', 'test_labels',
                                 'descriptor_scaler']
        elif data_type == 'scaled' and category == 'regression':
            pickle_file_names = ['train_descriptors', 'test_descriptors', 'train_target', 'test_target', 'descriptors',
                                 'target_scaler', 'descriptor_scaler']
        else:
            pickle_file_names = ['train_descriptors', 'test_descriptors', 'train_target', 'test_target', 'descriptors']

        return pickle_file_names

    def set_pickle_fixtures_path_in_context_object(self, category, data_type):
        """
        This function updated the paths in the context object with  the 'names' of
        the pickle objects one needs to get based on their test conditions

        Args:
            category (str): which category of data is being used. (regression, classification, etc)
            data_type (str): the folder within fixtures/category that is to be used
            See the funciton 'get_needed_pickle_file_names' for more details
        """

        # import settings and reload it - this makes the context paths dicitonary in the context object
        assert (os.path.isfile('settings.py'))
        import settings
        importlib.reload(settings)
        with settings.context as context:
            pickle_file_names = self.get_needed_pickle_file_names(category, data_type)
            for pickle_file_name in pickle_file_names:
                path_to_pickle_file = 'fixtures/{}_pkls/{}_data/{}.pkl'.format(category, data_type, pickle_file_name)
                context.context_paths.update({pickle_file_name: path_to_pickle_file})

    def tearDown(self):
        os.system('rm -rf .job*')
        os.system('rm settings.py')
        os.system('rm *.pyi')
        os.system('rm *.csv')

    @staticmethod
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


    def min_max_pass_condition(self, data):
        for col in data.T:
            self.assertAlmostEqual(1.0, np.amax(col))
            self.assertAlmostEqual(0.0, np.amin(col))

    def standard_scaler_pass_condition(self, data):
        column_means = data.mean(axis=0)
        column_standard_deviations = data.std(axis=0)
        for column_mean in column_means:
            self.assertAlmostEqual(0.0, column_mean)
        for column_standard_deviation in column_standard_deviations:
            self.assertAlmostEqual(1.0, column_standard_deviation)

    def remove_duplicates_pass_condition(self, data):
        data = pandas.DataFrame(data)
        self.assertFalse(data.duplicated().any())

    def remove_missing_pass_condition(self, data):
        data = pandas.DataFrame(data)
        self.assertFalse(data.isnull().values.any())

    def droppers_pass_conditions(self, data, flavor):
        if 'remove_missing' in flavor:
            self.remove_missing_pass_condition(data)
        elif 'remove_duplicates' in flavor:
            self.remove_duplicates_pass_condition(data)

    def run_scaler_flavor_test(self, category, flavor):
        self.set_pickle_fixtures_path_in_context_object(category, 'unscaled')
        shutil.copy(os.path.join(self.asset_path, flavor), flavor)
        os.system('python ' + flavor)
        train_target, train_descriptors, test_target, test_descriptors = self.load_test_train_targets_and_descriptors()
        # Check the pass conditions for each data loaded
        for data in [train_target, train_descriptors]:
            if 'min_max_scaler' in flavor:
                self.min_max_pass_condition(data)
            elif 'standardization' in flavor:
                self.standard_scaler_pass_condition(data)


class TestPreProcessingScalerFlavors(BaseUnitTest):
    """
    This class performs unittests for the pre_processing sclaer flavors.
    We may only check regression data here, and assume it would work for the other data categories.
    """

    params = [
        ['regression', "pyml:pre_processing:min_max_scaler:sklearn.pyi"],
        ['regression', "pyml:pre_processing:standardization:sklearn.pyi"],
    ]
    @parameterized.expand(params)
    def test_flavor(self, category, flavor):
        self.custom_setup(category)
        self.run_scaler_flavor_test(category, flavor)


class TestPreProcessingDroppers(BaseUnitTest):
    """
    This class performs unittests for the pre_processing sclaer flavors.
    """

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

        import settings
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
        train_target, train_descriptors, test_target, test_descriptors = self.load_test_train_targets_and_descriptors()

        # Check the pass conditions for each data loaded
        for data in [train_target, train_descriptors, test_target, test_descriptors]:
            self.droppers_pass_conditions(data, flavor)


if __name__ == '__main__':
    unittest.main()
