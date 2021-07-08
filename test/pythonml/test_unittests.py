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


class TestConfigs:
    """
    This class give easy access to the info stored in the .yaml files
    """

    def __init__(self, yaml_configuration_file):
        self.configuration = self.get_yaml_configs(yaml_configuration_file)
        self.asset_path = self.configuration["asset_path"]
        self.fixtures_path = self.configuration["fixtures"]["path"]
        self.settings_filename = self.configuration["fixtures"]["settings"]
        self.unit_shortnames = self.configuration["unit_shortnames"]
        self.files_to_remove = self.configuration["files_to_remove"]
        self.extensions_to_remove = self.configuration["extensions_to_remove"]

    @staticmethod
    def get_yaml_configs(yaml_configuration_file):
        with open(yaml_configuration_file, "r") as yaml_configs:
            yaml_file_contents = yaml.safe_load(yaml_configs)
        return yaml_file_contents

    def get_train_predict_set_names(self, category):
        assert(category in ['regression', 'classification', 'clustering'])
        training_set_name = self.configuration["fixtures"][category]["training_set_name"]
        predict_set_name = self.configuration["fixtures"][category]["predict_set_name"]
        return training_set_name, predict_set_name

    def get_test_info(self, category, info_needed):
        all_tests = self.configuration["tests"]
        configurations = [i for i in all_tests.items() if i[1]["category"] == category]
        info_in_category = [i[1][info_needed] for i in configurations][0]
        info_for_run = [[info] for info in info_in_category]
        return info_for_run


class PassConditions(unittest.TestCase):
    """
    A class to help handle pass conditions for unittests
    """

    def assert_correct_pickles_made(self):
        for pickle in ['train_target.pkl', 'test_descriptors.pkl', 'train_target.pkl', 'test_descriptors.pkl']:
            self.assertTrue(os.path.exists(os.path.join('.job_context', pickle)))

    def assert_descriptors_pickle_made(self):
        self.assertTrue(os.path.exists(os.path.join('.job_context', 'descriptors.pkl')))

    def assert_read_csv_makes_correct_train_target(self, category='regression'):
        """
        We check that the operations to the train target in read csv really happen.
        We perform the same operations to the raw data and check that the data is
        the same in the end
        """

        # we have to import and reload settings here to update anything related to settings
        import settings
        importlib.reload(settings)
        data = pandas.read_csv(settings.datafile)
        if category == 'clustering':
            target = data.to_numpy()[:, 0]
        else:
            target = data.pop(settings.target_column_name).to_numpy()
        target = target.reshape(-1, 1)
        target_from_pkl = settings.context.load('train_target')
        self.assertIsNone(np.testing.assert_array_equal(target_from_pkl, target))

    def assert_read_csv_makes_correct_descriptors(self):
        """
        We check that the operations to the descriptors in read csv really happen.
        We perform the same operations to the raw data and check that the data is
        the same in the end
        """

        # we have to import and reload settings here to update anything related to settings
        import settings
        importlib.reload(settings)
        data = pandas.read_csv(settings.datafile)
        descriptors = data.to_numpy()
        descriptors_from_pkl = settings.context.load('descriptors')
        self.assertIsNone(np.testing.assert_array_equal(descriptors_from_pkl, descriptors))

    def pass_condition_standard_scaler(self, data):
        """
        check that 'data' meets the standard scaler pass condition:
        """

        column_means = data.mean(axis=0)
        column_standard_deviations = data.std(axis=0)
        for column_mean in column_means:
            self.assertAlmostEqual(0.0, column_mean)
        for column_standard_deviation in column_standard_deviations:
            self.assertAlmostEqual(1.0, column_standard_deviation)

    def pass_condition_minmax_scaler(self, data):
        """
        check that 'data' meets the min max pass condition:
        """

        for col in data.T:
            self.assertAlmostEqual(1.0, np.amax(col))
            self.assertAlmostEqual(0.0, np.amin(col))

    def pass_condition_remove_missing(self, data):
        """
        check that 'data' does not contain any np.nan values
        """

        data = pandas.DataFrame(data)
        self.assertFalse(data.isnull().values.any())

    def pass_condition_remove_duplicates(self, data):
        """
        check that 'data' does not contain any duplicate rows
        """

        data = pandas.DataFrame(data)
        self.assertFalse(data.duplicated().any())


class BaseUnitTest(unittest.TestCase):
    """
    Base class for the unittests. Each unittest in this file will inherit this class. This class
    'sets up' each unit test and tears it down.
    It sets up the unit test by getting settings.py from fixtures and editing for the test to be done.
    It also gives access to the TestConfigs and PassConditions class objects as attributes
    """

    category = ''
    test_configs = TestConfigs('unittest_configuration.yaml')
    pass_conditions = PassConditions()

    def setUp(self):
        self.asset_path = self.test_configs.asset_path
        self.fixtures_path = self.test_configs.fixtures_path
        self.settings_filename = self.test_configs.settings_filename
        with open(os.path.join(self.fixtures_path, self.settings_filename), "r") as inp, \
                open(self.settings_filename, "w") as outp:
            for line in inp:
                # Users can select the type of problem category in the settings.py file. Normally, it is set to
                # "regression" by default, but to make the regex more convenient, the settings.py file in fixtures
                # has this value set to "PROBLEM_CATEGORY_HERE"
                line = re.sub("PROBLEM_CATEGORY_HERE", self.category, line)
                outp.write(line)

        training_file, predict_file = self.test_configs.get_train_predict_set_names(self.category)
        shutil.copy(os.path.join(self.fixtures_path, training_file), "data_to_train_with.csv")
        shutil.copy(os.path.join(self.fixtures_path, predict_file), "data_to_predict_with.csv")
        # Each time we reload settings, we re-initialize the context object, which takes the .job_context
        # directory that may have just gotten 'tearedDown' - setting the unittest fresh each time.
        import settings
        importlib.reload(settings)

    def get_flavor_file(self, unit_shortname):
        return self.test_configs.unit_shortnames[unit_shortname]

    def copy_unit(self, unit_shortname):
        unit_to_copy = self.test_configs.unit_shortnames[unit_shortname]
        shutil.copy(self.asset_path + unit_to_copy, unit_to_copy)

    def run_unit(self, unit_shortname):
        unit_to_run = self.test_configs.unit_shortnames[unit_shortname]
        os.system('python ' + unit_to_run)

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
    def load_test_train_targets_and_descriptors():
        """
        Loads a set of commonly used pickle files from an updated location in the context object
        """

        import settings
        importlib.reload(settings)
        train_target = settings.context.load("train_target")
        train_descriptors = settings.context.load("train_descriptors")
        test_target = settings.context.load("test_target")
        test_descriptors = settings.context.load("test_descriptors")
        return train_target, train_descriptors, test_target, test_descriptors

    @staticmethod
    def set_test_split_in_train_test_spit_file(train_test_split_file, test_split=0.2):
        """
        Updates the train test split unit with the test split ration
        Args:
            train_test_split_file (str): filename of the train test split flavor
            test_split (float): the ratio at which the data will be split for testing
        """

        with open(train_test_split_file, 'r') as input_file:
            input_filelines = input_file.readlines()
        with open(train_test_split_file, 'w') as output_file:
            for line in input_filelines:
                line = re.sub("{{ mlTrainTestSplit.fraction_held_as_test_set }}", str(test_split), line)
                output_file.write(line)

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
        for file in os.listdir():
            if (file in self.test_configs.files_to_remove) or any([file.endswith(ext) for ext in self.test_configs.extensions_to_remove]):
                try:
                    os.remove(file)
                except (IsADirectoryError, PermissionError):
                    shutil.rmtree(file)
                except FileNotFoundError:
                    pass


class TestIOReadCSVRegression(BaseUnitTest):
    """
    Unit tests for the read_csv flavor. This test considers reading regression data in fixtures
    """

    category = 'regression'
    flavors_to_be_tested = BaseUnitTest.test_configs.get_test_info('io_read_csv_'+category, 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_correct_pickles_made(self, flavor):
        self.copy_unit(flavor)
        flavor_file = self.get_flavor_file(flavor)
        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + flavor_file)
                self.pass_conditions.assert_descriptors_pickle_made()
            else:
                os.system('python ' + flavor_file)
                self.pass_conditions.assert_correct_pickles_made()

    @parameterized.expand(flavors_to_be_tested)
    def test_correct_data_stored_regression(self, flavor):
        self.copy_unit(flavor)
        flavor_file = self.get_flavor_file(flavor)
        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + flavor_file)
                self.pass_conditions.assert_read_csv_makes_correct_descriptors()
            else:
                os.system('python ' + flavor_file)
                self.pass_conditions.assert_read_csv_makes_correct_train_target(self.category)


class TestIOReadCSVClassification(BaseUnitTest):
    """
    Unit tests for the read_csv flavor. This test considers reading classification data in fixtures
    """

    category = 'classification'
    flavors_to_be_tested = BaseUnitTest.test_configs.get_test_info('io_read_csv_'+category, 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_correct_data_stored_classification(self, flavor):
        self.copy_unit(flavor)
        flavor_file = self.get_flavor_file(flavor)
        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + flavor_file)
                self.pass_conditions.assert_read_csv_makes_correct_descriptors()
            else:
                os.system('python ' + flavor_file)
                self.pass_conditions.assert_read_csv_makes_correct_train_target(self.category)


class TestIOReadCSVClustering(BaseUnitTest):
    """
    Unit tests for the read_csv flavor. This test considers reading clustering data in fixtures
    """

    category = 'clustering'
    flavors_to_be_tested = BaseUnitTest.test_configs.get_test_info('io_read_csv_'+category, 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_correct_data_stored_clustering(self, flavor):
        self.copy_unit(flavor)
        flavor_file = self.get_flavor_file(flavor)
        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + flavor_file)
                self.pass_conditions.assert_read_csv_makes_correct_descriptors()
            else:
                os.system('python ' + flavor_file)
                self.pass_conditions.assert_read_csv_makes_correct_train_target(self.category)


class TestPreProcessingScalers(BaseUnitTest):
    """
    This class performs unittests for the pre_processing sclaer flavors.
    We may only check regression data here, and assume it would work for the other data categories.
    """

    category = 'regression'
    flavors_to_be_tested = BaseUnitTest.test_configs.get_test_info('pre_processing_scalers', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):
        self.set_pickle_fixtures_path_in_context_object(self.category, 'unscaled')

        # 1. Copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        self.copy_unit(flavor)
        self.run_unit(flavor)

        # Load the (hopefully) modified data in .job_context. We need to reload settings to see whats in .job_context
        # after running the model, here
        import settings
        importlib.reload(settings)
        train_target, train_descriptors, test_target, test_descriptors = self.load_test_train_targets_and_descriptors()

        # Check the pass conditions for each data loaded
        for data in [train_target, train_descriptors]:
            if 'minMax' in flavor:
                self.pass_conditions.pass_condition_minmax_scaler(data)
            if 'standScale' in flavor:
                self.pass_conditions.pass_condition_standard_scaler(data)


class TestPreProcessingDroppers(BaseUnitTest):
    """
    This class performs unittests for the pre_processing sclaer flavors.
    We may only check regression data here, and assume it would work for the other data categories.
    """

    category = 'regression'
    flavors_to_be_tested = BaseUnitTest.test_configs.get_test_info('pre_processing_droppers', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):

        self.set_pickle_fixtures_path_in_context_object(self.category, 'unscaled')

        # 1. Copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        self.copy_unit(flavor)
        self.run_unit(flavor)

        # Load the (hopefully) modified data in .job_context. We need to reload settings to see whats in .job_context
        # after running the model, here
        import settings
        importlib.reload(settings)
        train_target, train_descriptors, test_target, test_descriptors = self.load_test_train_targets_and_descriptors()

        # Check the pass conditions for each data loaded
        for data in [train_target, train_descriptors]:
            if 'dropDupes' in flavor:
                self.pass_conditions.pass_condition_remove_duplicates(data)
            if 'dropMissing' in flavor:
                self.pass_conditions.pass_condition_remove_missing(data)


class TestModelFlavorsRegression(BaseUnitTest):
    """
    This class performs unit tests for the model flavors in the 'regression' category
    """

    category = 'regression'
    flavors_to_be_tested = BaseUnitTest.test_configs.get_test_info('model_regression', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):

        self.set_pickle_fixtures_path_in_context_object(self.category, 'scaled')
        # copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        self.copy_unit(flavor)

        # train
        self.run_unit(flavor)
        import settings
        importlib.reload(settings)
        with settings.context as context:
            rmse = context.load('RMSE')
        assert(rmse <= 2*0.1)

        # predict
        self.set_to_predict_phase()
        self.run_unit(flavor)
        assert(os.path.isfile('predictions.csv'))


class TestModelFlavorsClassification(BaseUnitTest):
    """
    This class performs unit tests for the model flavors in the 'classification' category
    """

    category = 'classification'
    flavors_to_be_tested = BaseUnitTest.test_configs.get_test_info('model_classification', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):

        self.set_pickle_fixtures_path_in_context_object(self.category, 'scaled')
        # copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        self.copy_unit(flavor)

        # train
        self.run_unit(flavor)
        import settings
        importlib.reload(settings)
        with settings.context as context:
            confusion_matrix = context.load('confusion_matrix')
        accuracy = confusion_matrix.diagonal()/confusion_matrix.sum(axis=0)
        assert(accuracy.all() >= 0.6)

        # predict
        self.set_to_predict_phase()
        self.run_unit(flavor)
        assert(os.path.isfile('predictions.csv'))
        

class TestModelFlavorsClustering(BaseUnitTest):
    """
    This class performs unit tests for the model flavors in the 'clustering' category
    """
    
    category = 'clustering'
    flavors_to_be_tested = BaseUnitTest.test_configs.get_test_info('model_clustering', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):

        self.set_pickle_fixtures_path_in_context_object(self.category, 'scaled')
        # copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        self.copy_unit(flavor)

        # train
        self.run_unit(flavor)

        # predict
        self.set_to_predict_phase()
        self.run_unit(flavor)
        assert(os.path.isfile('predictions.csv'))


class TestPostProcessingRegression(BaseUnitTest):
    """
    This class performs unittests for post processing flavor that considers regression data
    """

    category = 'regression'
    flavors_to_be_tested_regression = BaseUnitTest.test_configs.get_test_info('post_processing_regression', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested_regression)
    def test_flavor(self, flavor):
        # set the paths to the pickle files in context_paths dictionary in conext object
        self.set_pickle_fixtures_path_in_context_object(self.category, 'model')
        # copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        self.copy_unit(flavor)
        # run unit
        self.run_unit(flavor)
        # assert
        assert(os.path.isfile('my_parity_plot.png'))


class TestPostProcessingClassification(BaseUnitTest):
    """
    This class performs unittests for post processing flavor that considers classification data
    """

    category = 'classification'
    flavors_to_be_tested_regression = BaseUnitTest.test_configs.get_test_info('post_processing_classification', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested_regression)
    def test_flavor(self, flavor):
        # set the paths to the pickle files in context_paths dictionary in conext object
        self.set_pickle_fixtures_path_in_context_object(self.category, 'model')
        # copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        self.copy_unit(flavor)
        # run unit
        self.run_unit(flavor)
        # assert
        assert(os.path.isfile('my_roc_curve.png'))


class TestPostProcessingClustering(BaseUnitTest):
    """
    This class performs unittests for post processing flavor that considers clustering data
    """

    category = 'clustering'
    flavors_to_be_tested_regression = BaseUnitTest.test_configs.get_test_info('post_processing_clustering', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested_regression)
    def test_flavor(self, flavor):
        # set the paths to the pickle files in context_paths dictionary in conext object
        self.set_pickle_fixtures_path_in_context_object(self.category, 'model')
        # copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        self.copy_unit(flavor)
        # run unit
        self.run_unit(flavor)
        # assert
        assert(os.path.isfile('train_clusters.png'))
        assert (os.path.isfile('test_clusters.png'))


if __name__ == '__main__':
    unittest.main()