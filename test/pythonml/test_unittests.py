#!/usr/bin/env python
import importlib
import os
import re
import shutil
import unittest
import functools
import yaml
from parameterized import parameterized, param
import pandas
import numpy as np
from typing import Dict, List, Any, Tuple, Callable


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
        self.files_to_remove = self.configuration["files_to_remove"]
        self.extensions_to_remove = self.configuration["extensions_to_remove"]
        self.category = ''

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

    def copy_units(self, unit_shortnames):
        for unit_shortname in unit_shortnames:
            unit_to_copy = self.unit_shortnames[unit_shortname[0]]
            shutil.copy(self.asset_path + unit_to_copy, unit_to_copy)

    def run_units(self, unit_shortnames):
        for unit_shortname in unit_shortnames:
            unit_to_run = self.unit_shortnames[unit_shortname[0]]
            os.system('python '+ unit_to_run)

    def set_test_split_in_train_test_spit_file(self, train_test_split_file, test_split=0.2):
        with open(train_test_split_file, 'r') as input_file:
            input_filelines = input_file.readlines()
        with open(train_test_split_file, 'w') as output_file:
            for line in input_filelines:
                line = re.sub("{{ mlTrainTestSplit.fraction_held_as_test_set }}", str(test_split), line)
                output_file.write(line)


unittest_helper = TestHelper('unittest_configuration.yaml')

class Base(unittest.TestCase):

    asset_path = unittest_helper.asset_path
    fixtures_path = unittest_helper.fixtures_path
    settings_filename = unittest_helper.settings_filename

    def setup(self, category):
        '''
        custom setup
        '''
        self.category = category
        #print('in setup - self.category = ', self.category)
        with open(os.path.join(self.fixtures_path, self.settings_filename), "r") as inp, open(self.settings_filename, "w") as outp:
            for line in inp:
                # Users can select the type of problem category in the settings.py file. Normally, it is set to
                # "regression" by default, but to make the regex more convenient, the settings.py file in fixtures
                # has this value set to "PROBLEM_CATEGORY_HERE"
                line = re.sub("PROBLEM_CATEGORY_HERE", self.category, line)
                outp.write(line)

        training_file, predict_file = unittest_helper.get_train_predict_set_names(self.category)
        shutil.copy(os.path.join(self.fixtures_path, training_file), "data_to_train_with.csv")
        shutil.copy(os.path.join(self.fixtures_path, predict_file), "data_to_predict_with.csv")
        # Each time we reload settings, we re-initialize the context object, which takes the .job_context
        # directory that may have just gotten 'tearedDown' - setting the unittest fresh each time.
        import settings; importlib.reload(settings)

    @staticmethod
    def load_test_train_targets_and_descriptors():
        assert(os.path.isfile('settings.py'))
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
        os.system('rm -rf .job_context')
        os.system('rm -rf settings.py')
        os.system('rm -rf *.csv')
        os.system('rm -rf *.pyi')
        os.system('rm -rf *.png')


class PassConditions(unittest.TestCase):
    """
    A class to help handle pass conditions for unittests
    """

    def assert_train_test_target_descriptors_exist(self):
        self.assertTrue(os.path.exists(os.path.join('.job_context', 'train_target.pkl')))
        self.assertTrue(os.path.exists(os.path.join('.job_context', 'test_descriptors.pkl')))
        self.assertTrue(os.path.exists(os.path.join('.job_context', 'train_target.pkl')))
        self.assertTrue(os.path.exists(os.path.join('.job_context', 'test_descriptors.pkl')))

    def assert_descriptors_exist(self):
        self.assertTrue(os.path.exists(os.path.join('.job_context', 'descriptors.pkl')))

    def check_read_csv_correct_pickles_generated(self, do_predict):
        if do_predict:
            self.assert_descriptors_exist()
        else:
            self.assert_train_test_target_descriptors_exist()

    def check_read_csv_correct_data_stored(self, do_predict, category='regression'):
        import settings; importlib.reload(settings)
        data = pandas.read_csv(settings.datafile)
        if do_predict:
            descriptors = data.to_numpy()
            descriptors_from_pkl = settings.context.load('descriptors')
            self.assertIsNone(np.testing.assert_array_equal(descriptors_from_pkl, descriptors))
        else:
            if category == 'clustering':
                target = data.to_numpy()[:, 0]
            else:
                target = data.pop(settings.target_column_name).to_numpy()
            target = target.reshape(-1, 1)
            target_from_pkl = settings.context.load('train_target')
            self.assertIsNone(np.testing.assert_array_equal(target_from_pkl, target))

    def check_scaler_pass_conditions(self, data, flavor):
        if 'minMax' in flavor:
            # min max condition: columns have min of 0 and max of 1
            for col in data.T:
                self.assertAlmostEqual(1.0, np.amax(col))
                self.assertAlmostEqual(0.0, np.amin(col))
        elif 'standScale' in flavor:
            # standard scaler condition: Columns have mean of 0 and standard_deviation of 1
            column_means = data.mean(axis=0)
            column_standard_deviations = data.std(axis=0)
            for column_mean in column_means:
                self.assertAlmostEqual(0.0, column_mean)
            for column_standard_deviation in column_standard_deviations:
                self.assertAlmostEqual(1.0, column_standard_deviation)

    def check_dropper_pass_conditions(self, data, flavor):
        # turn the data into data frames
        data_frame = pandas.DataFrame(data)
        if 'Missing' in flavor:
            self.assertFalse(data_frame.isnull().values.any())
        elif 'Dupes' in flavor:
            self.assertFalse(data_frame.duplicated().any())

    def check_model_pass_conditions(self, do_predict, category='regression'):
        if do_predict:
            assert (os.path.isfile('predictions.csv'))
        else:
            if category == 'clustering':
                assert(os.path.isfile(os.path.join('.job_context', 'train_labels.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_labels.pkl')))
            else:
                assert(os.path.isfile(os.path.join('.job_context', 'train_predictions.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_predictions.pkl')))
                if category == 'regression':
                    assert(os.path.isfile(os.path.join('.job_context', 'RMSE.pkl')))
                elif category == 'classification':
                    assert(os.path.isfile(os.path.join('.job_context', 'test_probabilities.pkl')))
                    assert(os.path.isfile(os.path.join('.job_context', 'confusion_matrix.pkl')))

    def check_post_processing_pass_conditions(self, category='regression'):
        if category == 'regression':
            self.assertTrue(os.path.exists('my_parity_plot.png'))
        elif category == 'classification':
            self.assertTrue(os.path.exists('my_roc_curve.png'))
        elif category == 'clustering':
            self.assertTrue(os.path.exists('train_test_split.png'))
            self.assertTrue(os.path.exists('test_clusters.png'))


pass_conditions = PassConditions()


# define some tests that we can use in the unittests to avoid lots of repeating code
def read_csv_correct_data_stored(self, flavor):
    flavor_file = unittest_helper.unit_shortnames[flavor]
    shutil.copy(self.asset_path + flavor_file, flavor_file)
    for do_predict in [False, True]:
        if do_predict:
            self.set_to_predict_phase()
            os.system('python ' + flavor_file)
            pass_conditions.check_read_csv_correct_data_stored(do_predict, self.category)
        else:
            os.system('python ' + flavor_file)
            pass_conditions.check_read_csv_correct_data_stored(do_predict, self.category)


class TestIOReadCSVFlavor(Base):
    """
    This class performs unittests for the io read csv flavor.
    The first test is to see if the correct pickles are generated and is only need to be done for the
    regression data because the pickle generation is indifferent to the data category
    """

    flavors_to_be_tested = unittest_helper.get_test_info('io_read_csv_regression', 'units_to_run')
    @parameterized.expand(flavors_to_be_tested)
    def test_correct_pickles_generated(self, flavor):
        self.setup('regression')
        flavor_file = unittest_helper.unit_shortnames[flavor]
        shutil.copy(self.asset_path + flavor_file, flavor_file)
        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + flavor_file)
                pass_conditions.check_read_csv_correct_pickles_generated(do_predict)
            else:
                os.system('python ' + flavor_file)
                pass_conditions.check_read_csv_correct_pickles_generated(do_predict)

    @parameterized.expand(flavors_to_be_tested)
    def test_correct_data_stored_regression(self, flavor):
        self.setup('regression')
        read_csv_correct_data_stored(self, flavor)

    @parameterized.expand(flavors_to_be_tested)
    def test_correct_data_stored_classification(self, flavor):
        self.setup('classification')
        read_csv_correct_data_stored(self, flavor)

    @parameterized.expand(flavors_to_be_tested)
    def test_correct_data_stored_clustering(self, flavor):
        self.setup('clustering')
        read_csv_correct_data_stored(self, flavor)



class TestPreProcessingScalersRegression(Base):
    """
    This class performs unittests for the pre processing sclaer flavors that utilize regression data
    """

    pre_requisites_flavors = unittest_helper.get_test_info('pre_processing_scalers_regression', 'pre_requisites')
    flavors_to_be_tested = unittest_helper.get_test_info('pre_processing_scalers_regression', 'units_to_run')
    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):
        self.setup('regression')
        # 1. Copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
        unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])
        if ['IO_ttSplit'] in self.pre_requisites_flavors:
            unittest_helper.set_test_split_in_train_test_spit_file('pyml:data_input:train_test_split:sklearn.pyi', test_split=0.2)
        unittest_helper.run_units(self.pre_requisites_flavors)
        unittest_helper.run_units([[flavor]])
        # Load the (hopefully) modified data in .job_context\
        train_target, train_descriptors, test_target, test_descriptors = self.load_test_train_targets_and_descriptors()
        # Check the pass conditions for each data loaded
        for data in [train_target, train_descriptors]:
            pass_conditions.check_scaler_pass_conditions(data, flavor)


class TestPreProcessingDroppersRegression(Base):
    """
    This class performs unittests for the pre processing dropper flavors that utilize regression data
    """
    pre_requisites_flavors = unittest_helper.get_test_info('pre_processing_droppers_regression', 'pre_requisites')
    flavors_to_be_tested = unittest_helper.get_test_info('pre_processing_droppers_regression', 'units_to_run')
    @parameterized.expand(flavors_to_be_tested)
    def test_flavor(self, flavor):
        self.setup('regression')
        unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])
        if ['IO_ttSplit'] in self.pre_requisites_flavors:
            unittest_helper.set_test_split_in_train_test_spit_file('pyml:data_input:train_test_split:sklearn.pyi', test_split=0.2)
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
        for data in [train_target, train_descriptors]:
            pass_conditions.check_dropper_pass_conditions(data, flavor)


def run_model_check_correct_output(self, flavor):

    # 1. Copy pre_reqs and flavor file, then run the pre_reqs, followed by the flavor
    unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])
    if ['IO_ttSplit'] in self.pre_requisites_flavors:
        unittest_helper.set_test_split_in_train_test_spit_file('pyml:data_input:train_test_split:sklearn.pyi',
                                                               test_split=0.2)
    # False should come before true because we are to train before predict
    for do_predict in [False, True]:
        if do_predict:
            self.set_to_predict_phase()
            unittest_helper.run_units(self.pre_requisites_flavors)
            unittest_helper.run_units([[flavor]])
            pass_conditions.check_model_pass_conditions(do_predict, self.category)
        else:
            unittest_helper.run_units(self.pre_requisites_flavors)
            unittest_helper.run_units([[flavor]])
            pass_conditions.check_model_pass_conditions(do_predict, self.category)


class TestModelFlavors(Base):
    """
    This class performs unittests for the model flavors in the 'regression' category
    """

    pre_requisites_flavors_regression = unittest_helper.get_test_info('model_regression', 'pre_requisites')
    flavors_to_be_tested_regression = unittest_helper.get_test_info('model_regression', 'units_to_run')
    @parameterized.expand(flavors_to_be_tested_regression )
    def test_flavor(self, flavor):
        self.setup('regression')
        self.pre_requisites_flavors = self.pre_requisites_flavors_regression
        run_model_check_correct_output(self, flavor)

    pre_requisites_flavors_classification = unittest_helper.get_test_info('model_classification', 'pre_requisites')
    flavors_to_be_tested_classification = unittest_helper.get_test_info('model_classification', 'units_to_run')
    @parameterized.expand(flavors_to_be_tested_classification)
    def test_flavor(self, flavor):
        self.setup('classification')
        self.pre_requisites_flavors = self.pre_requisites_flavors_classification
        run_model_check_correct_output(self, flavor)

    pre_requisites_flavors_clustering  = unittest_helper.get_test_info('model_clustering', 'pre_requisites')
    flavors_to_be_tested_clustering = unittest_helper.get_test_info('model_clustering', 'units_to_run')
    @parameterized.expand(flavors_to_be_tested_clustering)
    def test_flavor(self, flavor):
        self.setup('clustering')
        self.pre_requisites_flavors = self.pre_requisites_flavors_clustering
        run_model_check_correct_output(self, flavor)




def run_post_processing_and_check_output(self, flavor):
    # copy the pre_reqs and then the flavor to be tested
    unittest_helper.copy_units(self.pre_requisites_flavors + [[flavor]])
    if ['IO_ttSplit'] in self.pre_requisites_flavors:
        unittest_helper.set_test_split_in_train_test_spit_file('pyml:data_input:train_test_split:sklearn.pyi', test_split=0.2)
    # run flavor and assert its output
    unittest_helper.run_units(self.pre_requisites_flavors)
    unittest_helper.run_units([[flavor]])


class TestPostProcessing(Base):
    """
    This class performs unittests for the flavors in the 'post processing' category
    """

    flavors_to_be_tested_regression = unittest_helper.get_test_info('post_processing_regression', 'units_to_run')
    pre_requisites_flavors_regression = unittest_helper.get_test_info('post_processing_regression', 'pre_requisites')
    @parameterized.expand(flavors_to_be_tested_regression)
    def test_flavor(self, flavor):
        self.category = 'regression'
        self.setup(self.category)
        self.pre_requisites_flavors = self.pre_requisites_flavors_regression
        run_post_processing_and_check_output(self, flavor)

    flavors_to_be_tested_classification = unittest_helper.get_test_info('post_processing_classification', 'units_to_run')
    pre_requisites_flavors_classification = unittest_helper.get_test_info('post_processing_classification', 'pre_requisites')
    @parameterized.expand(flavors_to_be_tested_classification)
    def test_flavor(self, flavor):
        self.category = 'classification'
        self.setup(self.category)
        self.pre_requisites_flavors = self.pre_requisites_flavors_classification
        run_post_processing_and_check_output(self, flavor)

    flavors_to_be_tested_clustering = unittest_helper.get_test_info('post_processing_clustering', 'units_to_run')
    pre_requisites_flavors_clustering = unittest_helper.get_test_info('post_processing_clustering', 'pre_requisites')
    @parameterized.expand(flavors_to_be_tested_clustering)
    def test_flavor(self, flavor):
        self.category = 'clustering'
        self.setup(self.category)
        self.pre_requisites_flavors = self.pre_requisites_flavors_clustering
        run_post_processing_and_check_output(self, flavor)


if __name__ == '__main__':
    unittest.main()
