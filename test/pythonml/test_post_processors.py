#!/usr/bin/env python
import importlib
import os
import re
import shutil
import unittest
import functools
import yaml
from parameterized import parameterized
import pandas
import numpy as np


class BaseUnitTest(unittest.TestCase):
    """
    Base class for the unittests. Each unittest in this file will inherit this class. This class
    'sets up' each unit test and tears it down.
    It sets up the unit test by getting settings.py from fixtures and editing for the test to be done.
    It also gives access to the TestConfigs and PassConditions class objects as attributes
    """

    asset_path = '../../assets/python/ml'
    fixtures_path = 'fixtures'
    settings_filename = 'settings.py'

    def custom_setup(self, category):
        """
        this is a custom setup function
        """
        with open(os.path.join(self.fixtures_path, self.settings_filename), "r") as inp, \
                open(self.settings_filename, "w") as outp:
            for line in inp:
                # Users can select the type of problem category in the settings.py file. Normally, it is set to
                # "regression" by default, but to make the regex more convenient, the settings.py file in fixtures
                # has this value set to "category_HERE"
                line = re.sub("PROBLEM_CATEGORY_HERE", category, line)
                outp.write(line)

        training_file, predict_file = self.get_train_predict_set_names(category)
        shutil.copy(os.path.join(self.fixtures_path, training_file), "data_to_train_with.csv")
        shutil.copy(os.path.join(self.fixtures_path, predict_file), "data_to_predict_with.csv")
        # Each time we reload settings, we re-initialize the context object, which takes the .job_context
        # directory that may have just gotten 'tearedDown' - setting the unittest fresh each time.
        import settings
        importlib.reload(settings)

    @staticmethod
    def get_train_predict_set_names(category):
        if category == 'regression' or category == 'classificaiton':
            training_file = '{}_training_data.csv'.format(category)
            predict_file = '{}_predict_data.csv'.format(category)
        else:
            training_file = 'clustering_blobs.csv'
            predict_file = 'clustering_blobs.csv'
        return training_file, predict_file

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
        os.system('rm *.png')


    def run_flavor_test(self, category, flavor, plots):
        self.set_pickle_fixtures_path_in_context_object(category, 'model')
        shutil.copy(os.path.join(self.asset_path, flavor), flavor)
        os.system('python ' + flavor)
        for plot in plots:
            assert(os.path.isfile(plot))


class TestPostProcessingFlavors(BaseUnitTest):
    """
    This class performs unit tests for the post-processing flavors
    """

    params = [
        ['regression', 'pyml:post_processing:parity_plot:matplotlib.pyi', ['my_parity_plot.png']],
        ['classification', 'pyml:post_processing:roc_curve:sklearn.pyi', ['my_roc_curve.png']],
        ['clustering', 'pyml:post_processing:pca_2d_clusters:matplotlib.pyi', ['train_test_split.png',
                                                                               'train_clusters.png',
                                                                               'test_clusters.png']],
    ]
    @parameterized.expand(params)
    def test_post_processing_flavors(self, category, flavor, plots):
        self.custom_setup(category)
        self.run_flavor_test(category, flavor, plots)


if __name__ == '__main__':
    unittest.main()
