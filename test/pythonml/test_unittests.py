#!/usr/bin/env python
import importlib
import os
import re
import sys
import shutil
import unittest
import functools
import subprocess
import yaml
from parameterized import parameterized
import pandas
import numpy as np


class TestHelper:
    """
    A helper function for testing. This class give easy access to the info stored in the .yaml files
    """

    def __init__(self, yaml_configuration_file):
        self.configuration = self.get_yaml_configs(yaml_configuration_file)
        self.asset_path = self.configuration["asset_path"]
        self.fixtures_path = self.configuration["fixtures"]["path"]
        self.settings_filename = self.configuration["fixtures"]["settings"]
        self.unit_shortnames = self.configuration["unit_shortnames"]
        self.regression_training_file, self.regression_predict_file = self.get_train_predict_set_names('regression')
        self.classification_training_file, self.classification_predict_file = self.get_train_predict_set_names('classification')
        self.clustering_training_file, self.clustering_predict_file = self.get_train_predict_set_names('clustering')

    @staticmethod
    def get_yaml_configs(yaml_configuration_file):
        with open(yaml_configuration_file, "r") as yaml_configs:
            yaml_file_contents = yaml.safe_load(yaml_configs)
        return yaml_file_contents

    def get_train_predict_set_names(self, category):
        training_set_name = self.configuration["fixtures"][category]["training_set_name"]
        predict_set_name = self.configuration["fixtures"][category]["predict_set_name"]
        return training_set_name, predict_set_name

    def get_train_predict_set(self, category):
        if category == "regression":
            training_file = self.regression_training_file
            predict_file = self.regression_predict_file
        elif category == "classification":
            training_file = self.classification_training_file
            predict_file = self.classification_predict_file
        elif category == "clustering":
            training_file = self.clustering_training_file
            predict_file = self.clustering_predict_file
        else:
            training_file, predict_file = -1
        return training_file, predict_file

    def get_test_info(self, category, info_needed):
        """
        Args:
            info_needed (str): Any info needed for the unittests of a given category.
                Ex) category = 'model_regression', info_needed = 'units_to_run'

        Returns:
              info_for_run (list of lists): Each inner list contains a single unit, either
              to be run either as the flavor to be tested or its pre_requisites
        """
        all_tests = self.configuration["tests"]
        configurations = [i for i in all_tests.items() if i[1]["category"] == category]
        info_in_category = [i[1][info_needed] for i in configurations][0]
        info_for_run = [[info] for info in info_in_category]
        return info_for_run

    def copy_units(self, unit_shortnames):
        for unit_shortname in unit_shortnames:
            unit_to_copy = self.unit_shortnames[unit_shortname[0]]
            shutil.copy(self.asset_path + unit_to_copy, unit_to_copy)

    def run_units(self, unit_shortnames):
        for unit_shortname in unit_shortnames:
            unit_to_run = self.unit_shortnames[unit_shortname[0]]
            os.system('python '+ unit_to_run)


unittest_helper = TestHelper('unittest_configuration.yaml')

class Base(unittest.TestCase):

    category = ''
    asset_path = unittest_helper.asset_path
    fixtures_path = unittest_helper.fixtures_path
    settings_filename = unittest_helper.settings_filename

    def setUp(self) -> None:

        with open(os.path.join(self.fixtures_path, self.settings_filename), "r") as inp, open(self.settings_filename, "w") as outp:
            for line in inp:
                # Users can select the type of problem category in the settings.py file. Normally, it is set to
                # "regression" by default, but to make the regex more convenient, the settings.py file in fixtures
                # has this value set to "PROBLEM_CATEGORY_HERE"
                line = re.sub("PROBLEM_CATEGORY_HERE", self.category, line)
                outp.write(line)

        training_file, predict_file = unittest_helper.get_train_predict_set(self.category)
        shutil.copy(os.path.join(self.fixtures_path, training_file), "data_to_train_with.csv")
        shutil.copy(os.path.join(self.fixtures_path, predict_file), "data_to_predict_with.csv")
        # Each time we reload settings, we re-initialize the context object, which takes the .job_context
        # directory that may have just gotten 'tearedDown' - setting the unittest fresh each time.
        import settings; importlib.reload(settings)

    @staticmethod
    def load_test_train_targets_and_descriptors():
        import settings; importlib.reload(settings)
        train_target = settings.context.load("train_target")
        train_descriptors = settings.context.load("train_descriptors")
        test_target = settings.context.load("test_target")
        test_descriptors = settings.context.load("test_descriptors")
        return train_target, train_descriptors, test_target, test_descriptors

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

    def tearDown(self):
        """
        A custom tear down class to be called after each time we test a flavor
        using 'prediction' instead of 'training'.
        """
        os.system('rm -rf .job_context')
        os.system('rm -rf pyml*')
        os.system('rm settings.py')
        os.system('rm *.csv')
        os.system('rm *.png')


class TestIOReadCSVRegression(Base):
    """
    This class performs unittests for the io read csv flavors that utilize regression data.
    The first test is to see if correct pickles are generated and is only need to be done for the
    regression data because the pickle generation is in different to the data category
    """

    category = 'regression'
    flavors_to_be_tested = unittest_helper.get_test_info('io_read_csv_regression', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_if_correct_pickles_generated(self, flavor):

        flavor_file = unittest_helper.unit_shortnames[flavor]
        # Copy flavor from assets
        shutil.copy(self.asset_path + flavor_file, flavor_file)

        for do_predict in [False, True]:

            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + flavor_file)
                assert (os.path.isfile(os.path.join('.job_context', 'descriptors.pkl')))
            else:
                os.system('python ' + flavor_file)
                assert(os.path.isfile(os.path.join('.job_context', 'train_target.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_descriptors.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'train_target.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_descriptors.pkl')))

    @parameterized.expand(flavors_to_be_tested)
    def test_correct_data_is_stored(self, flavor):

        flavor_file = unittest_helper.unit_shortnames[flavor]
        # Copy flavor from assets
        shutil.copy(self.asset_path + flavor_file, flavor_file)
        import settings
        data = pandas.read_csv(settings.datafile)

        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + flavor_file)
                importlib.reload(settings)
                descriptors_from_pkl = settings.context.load('descriptors')
                descriptors = data.to_numpy()
                self.assertIsNone(np.testing.assert_array_equal(descriptors_from_pkl, descriptors))
            else:
                os.system('python ' + flavor_file)
                importlib.reload(settings)
                target_from_pkl = settings.context.load('train_target')
                target = data.pop(settings.target_column_name).to_numpy()
                target = target.reshape(-1, 1)
                self.assertIsNone(np.testing.assert_array_equal(target_from_pkl, target))


class TestIOReadCSVClassification(Base):
    """
    This class performs unittests for the pre processing flavors that utilize regression data
    """

    category = 'classification'
    flavors_to_be_tested = unittest_helper.flavors_to_be_tested = unittest_helper.get_test_info('io_read_csv_classification', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_correct_data_is_stored(self, flavor):

        flavor_file = unittest_helper.unit_shortnames[flavor]
        # Copy flavor from assets
        shutil.copy(self.asset_path + flavor_file, flavor_file)

        import settings
        data = pandas.read_csv(settings.datafile)

        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + flavor_file)
                importlib.reload(settings)
                descriptors_from_pkl = settings.context.load('descriptors')
                descriptors = data.to_numpy()
                self.assertIsNone(np.testing.assert_array_equal(descriptors_from_pkl, descriptors))
            else:
                os.system('python ' + flavor_file)
                importlib.reload(settings)
                target_from_pkl = settings.context.load('train_target')
                target = data.pop(settings.target_column_name).to_numpy()
                target = target.reshape(-1, 1)
                self.assertIsNone(np.testing.assert_array_equal(target_from_pkl, target))


class TestIOReadCSVClustering(Base):
    """
    This class performs unittests for the pre processing flavors that utilize regression data
    """

    category = 'clustering'
    flavors_to_be_tested = unittest_helper.get_test_info('io_read_csv_clustering', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_correct_data_is_stored(self, flavor):

        flavor_file = unittest_helper.unit_shortnames[flavor]
        # Copy flavor from assets
        shutil.copy(self.asset_path + flavor_file, flavor_file)

        import settings
        data = pandas.read_csv(settings.datafile)

        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + flavor_file)
                importlib.reload(settings)
                descriptors_from_pkl = settings.context.load('descriptors')
                descriptors = data.to_numpy()
                self.assertIsNone(np.testing.assert_array_equal(descriptors_from_pkl, descriptors))
            else:
                os.system('python ' + flavor_file)
                importlib.reload(settings)
                target_from_pkl = settings.context.load('train_target')
                target = data.to_numpy()[:, 0]
                target = target.reshape(-1, 1)
                self.assertIsNone(np.testing.assert_array_equal(target_from_pkl, target))


class TestPreProcessingScalersRegression(Base):
    """
    This class performs unittests for the pre processing sclaer flavors that utilize regression data
    """

    category = 'regression'
    pre_requisites_flavors = unittest_helper.get_test_info('pre_processing_scalers_regression', 'pre_requisites')
    flavors_to_be_tested = unittest_helper.get_test_info('pre_processing_scalers_regression', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):

        # 1. Copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])
        unittest_helper.run_units(self.pre_requisites_flavors)
        unittest_helper.run_units([[flavor]])

        # Load the (hopefully) modified data in .job_context
        train_target, train_descriptors, test_target, test_descriptors = self.load_test_train_targets_and_descriptors()

        # Check the pass conditions for each data loaded
        for data in [train_target, train_descriptors, test_target, test_descriptors]:

            if 'minMax' in flavor:
                print('min_max')
                # min max condition: columns have min of 0 and max of 1
                for col in data.T:
                    self.assertAlmostEqual(1.0, np.amax(col))
                    self.assertAlmostEqual(0.0, np.amin(col))

            elif 'standScale' in flavor:
                print('standardization')
                # standard scaler condition: Columns have mean of 0 and standard_deviation of 1
                column_means = data.mean(axis=0)
                column_standard_deviations = data.std(axis=0)
                for column_mean in column_means:
                    self.assertAlmostEqual(0.0, column_mean)
                for column_standard_deviation in column_standard_deviations:
                    self.assertAlmostEqual(1.0, column_standard_deviation)


class TestPreProcessingDroppersRegression(Base):
    """
    This class performs unittests for the pre processing dropper flavors that utilize regression data
    """

    category = 'regression'
    pre_requisites_flavors = unittest_helper.get_test_info('pre_processing_droppers_regression', 'pre_requisites')
    flavors_to_be_tested = unittest_helper.get_test_info('pre_processing_droppers_regression', 'units_to_run')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):

        unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])

        # Make a pandas data frame with data formed during setUp in base class
        data = pandas.read_csv('data_to_train_with.csv')

        if 'Missing' in flavor:
            # Edit the data to be useful for this test. Insert 'np.nan' and bottom left and top right
            data.loc[4,'a'] = np.nan
            data.loc[0,'target'] = np.nan
        elif 'Dupes' in flavor:
            # Edit the data to be useful for this test. Duplicate the last row
            data = data.append(data.tail(1), ignore_index=True)

        # save it to csv again
        data.to_csv('data_to_train_with.csv', index=False)

        unittest_helper.run_units(self.pre_requisites_flavors)
        unittest_helper.run_units([[flavor]])

        # Load the (hopefully) modified data in .job_context
        train_target, train_descriptors, test_target, test_descriptors = self.load_test_train_targets_and_descriptors()

        # Check the pass conditions for each data loaded
        for data in [train_target, train_descriptors, test_target, test_descriptors]:

            # turn the data into data frames
            train_target_df = pandas.DataFrame(train_target)
            train_descriptors_df = pandas.DataFrame(train_descriptors)
            test_target_df = pandas.DataFrame(test_target)
            test_descriptors_df = pandas.DataFrame(test_descriptors)

            if 'Missing' in flavor:
                # assert that the data frames have met the test condition
                self.assertFalse(train_target_df.isnull().values.any())
                self.assertFalse(train_descriptors_df.isnull().values.any())
                self.assertFalse(test_target_df.isnull().values.any())
                self.assertFalse(test_descriptors_df.isnull().values.any())

            elif 'Dupes' in flavor:
                # assert that the data frames have met the test condition
                self.assertFalse(train_target_df.duplicated().any())
                self.assertFalse(train_descriptors_df.duplicated().any())
                self.assertFalse(test_target_df.duplicated().any())
                self.assertFalse(test_descriptors_df.duplicated().any())


class TestModelRegression(Base):
    """
    This class performs unittests for the model flavors in the 'regression' category
    """

    category = 'regression'
    flavors_to_be_tested = unittest_helper.get_test_info('model_regression', 'units_to_run')
    pre_requisites_flavors = unittest_helper.get_test_info('model_regression', 'pre_requisites')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):

        # 1. Copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])

        # False should come before true because we are to train before predict
        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                unittest_helper.run_units(self.pre_requisites_flavors)
                unittest_helper.run_units([[flavor]])
                assert(os.path.isfile('predictions.csv'))
            else:
                unittest_helper.run_units(self.pre_requisites_flavors)
                unittest_helper.run_units([[flavor]])
                assert(os.path.isfile(os.path.join('.job_context', 'RMSE.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'train_predictions.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_predictions.pkl')))


class TestModelClassification(Base):
    """
    This class performs unittests for the model flavors in the 'classification' category
    """

    category = 'classification'
    flavors_to_be_tested = unittest_helper.get_test_info('model_classification', 'units_to_run')
    pre_requisites_flavors = unittest_helper.get_test_info('model_classification', 'pre_requisites')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):

        # 1. Copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])

        # False should come before true because we are to train before predict
        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                unittest_helper.run_units(self.pre_requisites_flavors)
                unittest_helper.run_units([[flavor]])
                assert(os.path.isfile('predictions.csv'))
            else:
                unittest_helper.run_units(self.pre_requisites_flavors)
                unittest_helper.run_units([[flavor]])
                assert (os.path.isfile(os.path.join('.job_context', 'test_probabilities.pkl')))
                assert (os.path.isfile(os.path.join('.job_context', 'confusion_matrix.pkl')))
                assert (os.path.isfile(os.path.join('.job_context', 'train_predictions.pkl')))
                assert (os.path.isfile(os.path.join('.job_context', 'test_predictions.pkl')))


class TestModelClustering(Base):
    """
    This class performs unittests for the model flavors in the 'clustering' category
    """

    category = 'clustering'
    flavors_to_be_tested = unittest_helper.get_test_info('model_clustering', 'units_to_run')
    pre_requisites_flavors = unittest_helper.get_test_info('model_clustering', 'pre_requisites')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):

        # 1. Copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])

        # False should come before true because we are to train before predict
        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                unittest_helper.run_units(self.pre_requisites_flavors)
                unittest_helper.run_units([[flavor]])
                assert(os.path.isfile('predictions.csv'))
            else:
                unittest_helper.run_units(self.pre_requisites_flavors)
                unittest_helper.run_units([[flavor]])
                assert(os.path.isfile(os.path.join('.job_context', 'train_labels.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_labels.pkl')))


class TestPostProcessingRegression(Base):
    """
    This class performs unittests for the flavors in the 'post processing' category
    """
    category = 'regression'
    flavors_to_be_tested = unittest_helper.get_test_info('post_processing_regression', 'units_to_run')
    pre_requisites_flavors = unittest_helper.get_test_info('post_processing_regression', 'pre_requisites')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):
        # copy the pre_reqs and then the flavor to be tested
        unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])
        # run flavor and assert its output
        unittest_helper.run_units(self.pre_requisites_flavors)
        unittest_helper.run_units([[flavor]])
        assert(os.path.isfile('my_parity_plot.png'))


class TestPostProcessingClassification(Base):
    """
    This class performs unittests for the flavors in the 'post processing' category
    """
    category = 'classification'
    flavors_to_be_tested = unittest_helper.get_test_info('post_processing_classification', 'units_to_run')
    pre_requisites_flavors = unittest_helper.get_test_info('post_processing_classification', 'pre_requisites')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):
        # copy the pre_reqs and then the flavor to be tested
        unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])
        # run flavor and assert its output
        unittest_helper.run_units(self.pre_requisites_flavors)
        unittest_helper.run_units([[flavor]])
        assert(os.path.isfile('my_roc_curve.png'))


class TestPostProcessingClustering(Base):
    """
    This class performs unittests for the flavors in the 'post processing' category
    """
    category = 'clustering'
    flavors_to_be_tested = unittest_helper.get_test_info('post_processing_clustering', 'units_to_run')
    pre_requisites_flavors = unittest_helper.get_test_info('post_processing_clustering', 'pre_requisites')

    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):
        # copy the pre_reqs and then the flavor to be tested
        unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])
        # run flavor and assert its output
        unittest_helper.run_units(self.pre_requisites_flavors)
        unittest_helper.run_units([[flavor]])
        assert (os.path.isfile('train_test_split.png'))
        assert (os.path.isfile('test_clusters.png'))


if __name__ == '__main__':
    unittest.main()
