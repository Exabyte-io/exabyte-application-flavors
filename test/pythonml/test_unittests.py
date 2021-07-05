#!/usr/bin/env python
import importlib
import unittest
import os, shutil, sys
import re
import subprocess
import functools
import yaml
from parameterized import parameterized, param
from typing import Dict, List, Any, Tuple, Callable
import os
import unittest
import pandas
import numpy as np


with open("unittest_configuration.yaml", "r") as inp:
    configuration = yaml.safe_load(inp)

unit_shortnames = configuration["unit_shortnames"]

# ToDo: Refactor data clumps below into classes

# Figure out paths
asset_path = configuration["asset_path"]
fixtures_path = configuration["fixtures"]["path"]
settings_filename = configuration["fixtures"]["settings"]


# Get the path to the training data
def get_dataset_filenames(config: Dict[str, str]) -> Tuple[str, str]:
    """
    Given the configuration for a category of unit test (regression, classification, or clustering), extract out the
    filename of the training and predict test file. These correspond to the "training_set_name" and "predict_set_name"
    keys inside of the fixtures variable defined in integration_configuration.yaml. For example, if regression is
    chosen, "regression_training_data.csv" and "regression_predict_data.csv" will be returned.

    Args:
        config (Dict): Configuration extracted from fixtures in integration_configuration.yaml

    Returns:
        The filename of the training and predict set.
    """
    training_set_name = config["training_set_name"]
    predict_set_name = config["predict_set_name"]
    return training_set_name, predict_set_name


regression_training_file, regression_predict_file = get_dataset_filenames(
    configuration["fixtures"]["regression"])
classification_training_file, classification_predict_file = get_dataset_filenames(
    configuration["fixtures"]["classification"])
clustering_training_file, clustering_predict_file = get_dataset_filenames(
    configuration["fixtures"]["clustering"])
pre_processing_training_file, pre_processing_predict_file = regression_training_file, regression_predict_file

# Which files should we remove
files_to_remove = configuration["files_to_remove"]
extensions_to_remove = configuration["extensions_to_remove"]

# Extract the list of tests
def get_test_names_configs(configuration: List[Dict[str, Any]]) -> Tuple[List[List[str]], List[str]]:
    names = [i[0] for i in configuration]
    tests = [i[1]["units_to_run"] for i in configuration]
    return tests, names

all_tests = configuration["tests"]

regression_configs = [i for i in all_tests.items() if i[1]["category"] == "regression"]
tests_regression, names_regression = get_test_names_configs(regression_configs)
tests_regression = [[test] for test in tests_regression[0]]

classification_configs = [i for i in all_tests.items() if i[1]["category"] == "classification"]
tests_classification, names_classification = get_test_names_configs(classification_configs)
tests_classification = [[test] for test in tests_classification[0]]

clustering_configs = [i for i in all_tests.items() if i[1]["category"] == "clustering"]
tests_clustering, names_clustering = get_test_names_configs(clustering_configs)
tests_claustering = [[test] for test in tests_clustering[0]]

pre_processing_configs = [i for i in all_tests.items() if i[1]["category"] == "pre_processing"]
tests_pre_processing, names_regression = get_test_names_configs(pre_processing_configs)
tests_pre_processing = [[test] for test in tests_pre_processing[0]]

post_processing_configs = [i for i in all_tests.items() if i[1]["category"] == "post_processing"]
tests_post_processing, names_regression = get_test_names_configs(post_processing_configs)
tests_post_processing = [[test] for test in tests_post_processing[0]]


class Base(unittest.TestCase):

    category = ''

    def setUp(self) -> None:

        # default category
        if 'processing' in self.category:
            self.category = 'regression'

        with open(os.path.join(fixtures_path, settings_filename), "r") as inp, open(settings_filename, "w") as outp:
            for line in inp:
                # Users can select the type of problem category in the settings.py file. Normally, it is set to
                # "regression" by default, but to make the regex more convenient, the settings.py file in fixtures
                # has this value set to "PROBLEM_CATEGORY_HERE"
                line = re.sub("PROBLEM_CATEGORY_HERE", self.category, line)
                outp.write(line)

        if self.category == "regression":
            training_file = regression_training_file
            predict_file = regression_predict_file
        elif self.category == "classification":
            training_file = classification_training_file
            predict_file = classification_predict_file
        elif self.category == "clustering":
            training_file = clustering_training_file
            predict_file = clustering_predict_file
        else:
            training_file, predict_file = -1


        shutil.copy(os.path.join(fixtures_path, training_file), "data_to_train_with.csv")
        shutil.copy(os.path.join(fixtures_path, predict_file), "data_to_predict_with.csv")

        import settings; importlib.reload(settings)

        # Here, we have imported settings
        # if using the pickle method, set the paths to them
        with settings.context as context:
            context.context_paths.update({'train_descriptors': 'fixtures/'+self.category+'_pkls/train_descriptors.pkl',
                                          'test_descriptors': 'fixtures/'+self.category+'_pkls/test_descriptors.pkl',
                                          'train_target': 'fixtures/'+self.category+'_pkls/train_target.pkl',
                                          'test_target': 'fixtures/'+self.category+'_pkls/test_target.pkl',
                                          'descriptors': 'fixtures/'+self.category+'_pkls/descriptors.pkl',
                                          })
        # else, if using the generation methods, make the pickles - we can so this in the
        # flavor tests below or here


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

    @staticmethod
    def teardown():
        """
        A custom tear down class to be called after each time we test a flavor
        using 'prediction' instead of 'training'.
        """
        os.system('rm -rf .job_context')
        os.system('rm -rf pyml*')
        os.system('rm settings.py')
        os.system('rm *.csv')
        os.system('rm *.png')


class TestPreProcessingFlavors(Base):
    """
    This class performs unittests for the pre processing flavors
    """

    category = 'pre_processing'

    @parameterized.expand(tests_pre_processing)
    def test_flavor(self, flavor):

        # copy flavor
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])

        # we have to import settings and load a context object
        import settings
        context = settings.Context()

        # Here, this method does not use pickles, it is generative
        # Make a pandas data frame with data
        data = pandas.read_csv('data_to_train_with.csv')

        # get target and descriptors after custom manipulation of the data
        target = data.pop(settings.target_column_name).to_numpy()
        target = target.reshape(-1, 1)  # Reshape array from a row vector into a column vector
        descriptors = data.to_numpy()

        # save data as a pickle in .job_context using context
        # this updates keywords such as 'test_target' in the 'context_paths' dictionary
        # that may or may not have been established in the setUp in the Base class
        context.save(target, 'train_target')
        context.save(descriptors, 'train_descriptors')
        context.save(target, 'test_target')
        context.save(descriptors, 'test_descriptors')

        # run flavor - this write the (now) 'pre processed' data to .job_content
        os.system('python '+ unit_shortnames[flavor])

        # load the (hopefully) modified data in .job_context
        train_target = context.load("train_target")
        train_descriptors = context.load("train_descriptors")
        test_target = context.load("test_target")
        test_descriptors = context.load("test_descriptors")

        # Check the pass conditions
        for data in [train_target, train_descriptors, test_target, test_descriptors]:

            if 'min_max' in unit_shortnames[flavor]:
                print('min_max')
                # min max condition: columns have min of 0 and max of 1
                for col in data.T:
                    self.assertAlmostEqual(1.0, np.amax(col))
                    self.assertAlmostEqual(0.0, np.amin(col))

            elif 'standardization' in unit_shortnames[flavor]:
                print('standardization')
                # standard scaler condition: Columns have mean of 0 and standard_deviation of 1
                column_means = data.mean(axis=0)
                column_standard_deviations = data.std(axis=0)
                for column_mean in column_means:
                    self.assertAlmostEqual(0.0, column_mean)
                for column_standard_deviation in column_standard_deviations:
                    self.assertAlmostEqual(1.0, column_standard_deviation)

            # below converts the pass conditions for the remove_missing and remove_duplicates flavors
            elif 'remove' in unit_shortnames[flavor]:

                # turn the data into data frames
                train_target_df = pandas.DataFrame(train_target)
                train_descriptors_df = pandas.DataFrame(train_descriptors)
                test_target_df = pandas.DataFrame(test_target)
                test_descriptors_df = pandas.DataFrame(test_descriptors)

                if 'duplicate' in unit_shortnames[flavor]:
                    # assert that the data frames have met the test condition
                    self.assertFalse(train_target_df.duplicated().any())
                    self.assertFalse(train_descriptors_df.duplicated().any())
                    self.assertFalse(test_target_df.duplicated().any())
                    self.assertFalse(test_descriptors_df.duplicated().any())

                elif 'missing' in unit_shortnames[flavor]:
                    # assert that the data frames have met the test condition
                    self.assertFalse(train_target_df.isnull().values.any())
                    self.assertFalse(train_descriptors_df.isnull().values.any())
                    self.assertFalse(test_target_df.isnull().values.any())
                    self.assertFalse(test_descriptors_df.isnull().values.any())


class TestRegressionFlavors(Base):
    """
    This class performs unittests for the flavors in the 'regression' category
    """

    category = 'regression'

    @parameterized.expand(tests_regression)
    def test_flavor(self, flavor):
        # copy flavor
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])
        # False should come before true because we are to train before predict
        for do_predict in [False, True]:
            # run flavor
            if do_predict:
                self.set_to_predict_phase()
                os.system('python '+ unit_shortnames[flavor])
                # Assertions to be made after predicting
                assert(os.path.isfile('predictions.csv'))
                self.teardown()
            else:
                # Assertions to be made after training
                os.system('python '+ unit_shortnames[flavor])
                assert(os.path.isfile(os.path.join('.job_context', 'RMSE.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'train_predictions.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_predictions.pkl')))


class TestClassificationFlavors(Base):
    """
    This class performs unittests for the flavors in the 'classification' category
    """

    category = 'classification'

    @parameterized.expand(tests_classification)
    def test_flavor(self, flavor):
        # copy flavor
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])
        # False should come before true because we are to train before predict
        for do_predict in [False, True]:
            # run flavor
            if do_predict:
                self.set_to_predict_phase()
                os.system('python '+ unit_shortnames[flavor])
                # Assertions to be made after predicting
                assert(os.path.isfile('predictions.csv'))
                self.teardown()
            else:
                # Assertions to be made after training
                os.system('python '+ unit_shortnames[flavor])
                assert (os.path.isfile(os.path.join('.job_context', 'test_probabilities.pkl')))
                assert (os.path.isfile(os.path.join('.job_context', 'confusion_matrix.pkl')))
                assert (os.path.isfile(os.path.join('.job_context', 'train_predictions.pkl')))
                assert (os.path.isfile(os.path.join('.job_context', 'test_predictions.pkl')))


class TestClusteringFlavors(Base):
    """
    This class performs unittests for the flavors in the 'classification' category
    """

    category = 'clustering'

    @parameterized.expand(tests_clustering)
    def test_flavor(self, flavor):
        # copy flavor
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])
        # False should come before true because we are to train before predict
        for do_predict in [False, True]:
            # run flavor
            if do_predict:
                self.set_to_predict_phase()
                os.system('python '+ unit_shortnames[flavor])
                # Assertions to be made after predicting
                assert(os.path.isfile('predictions.csv'))
                self.teardown()
            else:
                # Assertions to be made after training
                os.system('python '+ unit_shortnames[flavor])
                assert(os.path.isfile(os.path.join('.job_context', 'train_labels.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_labels.pkl')))


class TestPostProcessingFlavors(Base):
    """
    This class performs unittests for the flavors in the 'post processing' category
    """

    category = 'post processing'

    @parameterized.expand(tests_post_processing)
    def test_flavor(self, flavor):
        # copy flavor
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])

        import settings

        if 'parity_plot' in unit_shortnames[flavor]:

            # the update to context_paths seems to take effect only after manager closes
            with settings.context as context:
                context.context_paths.update({'train_predictions': 'fixtures/regression_pkls/train_predictions.pkl',
                                              'test_predictions': 'fixtures/regression_pkls/test_predictions.pkl',})
            os.system('python ' + unit_shortnames[flavor])
            assert(os.path.isfile('my_parity_plot.png'))

        elif 'roc_curve' in unit_shortnames[flavor]:

            # the update to context_paths seems to take effect only after manager closes
            with settings.context as context:
                context.context_paths.update({'test_target': 'fixtures/classification_pkls/test_target.pkl',
                                              'test_probabilities': 'fixtures/classification_pkls/test_probabilities.pkl',})
            os.system('python ' + unit_shortnames[flavor])
            assert(os.path.isfile('my_roc_curve.png'))

        elif 'pca' in unit_shortnames[flavor]:

            with settings.context as context:
                context.context_paths.update({'train_labels': 'fixtures/clustering_pkls/train_labels.pkl',
                                              'test_labels': 'fixtures/clustering_pkls/test_labels.pkl',
                                              'train_descriptors': 'fixtures/clustering_pkls/train_descriptors.pkl',
                                              'test_descriptors': 'fixtures/clustering_pkls/test_descriptors.pkl',
                                              'descriptor_scaler': 'fixtures/clustering_pkls/descriptor_scaler.pkl', })

            os.system('python ' + unit_shortnames[flavor])
            assert(os.path.isfile('train_test_split.png'))
            assert(os.path.isfile('test_clusters.png'))


if __name__ == '__main__':
    unittest.main()
