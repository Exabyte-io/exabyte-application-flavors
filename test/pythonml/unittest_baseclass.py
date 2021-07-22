#!/usr/bin/env python
import importlib
import os
import re
import shutil
import unittest
import functools
import subprocess


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

        path_to_settings = os.path.join(self.fixtures_path, self.settings_filename)
        with open(path_to_settings, "r") as inp, \
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

        # We import and reload settings because we delete previous settings files on tearDown.
        # When we reload settings, we make a new context object
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

        names = ['']
        if data_type == 'model_data':
            if category == 'regression':
                names = ['train_predictions', 'test_predictions', 'train_target', 'test_target', 'target_scaler']
            elif category == 'classification':
                names = ['test_target', 'test_probabilities']
            elif category == 'clustering':
                names = ['train_descriptors', 'test_descriptors', 'train_labels', 'test_labels', 'descriptor_scaler']
        elif data_type == 'scaled_data' and category == 'regression':
            names = ['train_descriptors', 'test_descriptors', 'train_target', 'test_target', 'descriptors',
                     'target_scaler', 'descriptor_scaler']
        else:
            names = ['train_descriptors', 'test_descriptors', 'train_target', 'test_target', 'descriptors']
        return names

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
        assert os.path.isfile('settings.py')
        import settings
        importlib.reload(settings)
        with settings.context as context:
            pickle_file_names = self.get_needed_pickle_file_names(category, data_type)
            for pickle_file_name in pickle_file_names:
                path_to_pickle_file = 'fixtures/{}_pkls/{}/{}.pkl'.format(category, data_type, pickle_file_name)
                context.context_paths.update({pickle_file_name: path_to_pickle_file})

    def tearDown(self):
        for data in ['.job_context', 'settings.py', '*.png', '*.pyi', '*.csv']:
            subprocess.call('rm -rf '+data, shell=True)
