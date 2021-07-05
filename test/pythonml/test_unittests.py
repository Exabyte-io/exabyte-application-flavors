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
from typing import Dict, Tuple
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
def get_test_for_category(category):
    configurations = [i for i in all_tests.items() if i[1]["category"] == category]
    tests_in_category = [i[1]["units_to_run"] for i in configurations][0]
    tests_for_run = [[test] for test in tests_in_category]
    return tests_for_run

all_tests = configuration["tests"]

tests_io_read_csv_regression = get_test_for_category('io_read_csv_regression')
tests_io_read_csv_classification = get_test_for_category('io_read_csv_classification')
tests_io_read_csv_clustering = get_test_for_category('io_read_csv_clustering')

tests_pre_processing_regression = get_test_for_category('pre_processing_regression')

tests_model_regression = get_test_for_category('model_regression')
tests_model_classification = get_test_for_category('model_classification')
tests_model_clustering = get_test_for_category('model_clustering')

tests_post_processing_regression = get_test_for_category('post_processing_regression')
tests_post_processing_classification = get_test_for_category('post_processing_classification')
tests_post_processing_clustering = get_test_for_category('post_processing_clustering')


class Base(unittest.TestCase):

    category = ''

    def setUp(self) -> None:

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

        # if using the pickle method, set the paths to them
        # we need to reload because after the first tearDown, subsequent import to settings will not reinitialize
        # the context object and therefore will not remake the 'tearedDown' .job_context directory
        # In a way, each time we reload settings, we re-initialize the context object, which rakes the tearedDown
        # .job_context directory - setting the unittest fresh each time.
        import settings
        importlib.reload(settings)
        with settings.context as context:
            context.context_paths.update({'train_descriptors': 'fixtures/'+self.category+'_pkls/train_descriptors.pkl',
                                          'test_descriptors': 'fixtures/'+self.category+'_pkls/test_descriptors.pkl',
                                          'train_target': 'fixtures/'+self.category+'_pkls/train_target.pkl',
                                          'test_target': 'fixtures/'+self.category+'_pkls/test_target.pkl',
                                          'descriptors': 'fixtures/'+self.category+'_pkls/descriptors.pkl',
                                          })

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
    This class performs unittests for the io ead csv flavors that utilize regression data.
    The first test to see if correct pickles are generated, is only need to be done for the
    regression data because the pickle generation is in different to the data category
    """
    category = 'regression'
    @parameterized.expand(tests_io_read_csv_regression)
    def test_if_correct_pickles_generated(self, flavor):
        for do_predict in [False, True]:
            # Copy flavor from assets
            shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])
            if do_predict:
                self.set_to_predict_phase()
                os.system('python '+unit_shortnames[flavor])
                assert (os.path.isfile(os.path.join('.job_context', 'descriptors.pkl')))
            else:
                os.system('python '+unit_shortnames[flavor])
                assert(os.path.isfile(os.path.join('.job_context', 'train_target.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_descriptors.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'train_target.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_descriptors.pkl')))

    @parameterized.expand(tests_io_read_csv_regression)
    def test_correct_data_is_stored(self, flavor):
        import settings
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])
        data = pandas.read_csv(settings.datafile)
        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + unit_shortnames[flavor])
                importlib.reload(settings)
                descriptors_from_pkl = settings.context.load('descriptors')
                descriptors = data.to_numpy()
                self.assertIsNone(np.testing.assert_array_equal(descriptors_from_pkl, descriptors))
            else:
                os.system('python ' + unit_shortnames[flavor])
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
    @parameterized.expand(tests_io_read_csv_classification)
    def test_correct_data_is_stored(self, flavor):
        import settings
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])
        data = pandas.read_csv(settings.datafile)
        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + unit_shortnames[flavor])
                importlib.reload(settings)
                descriptors_from_pkl = settings.context.load('descriptors')
                descriptors = data.to_numpy()
                self.assertIsNone(np.testing.assert_array_equal(descriptors_from_pkl, descriptors))
            else:
                os.system('python ' + unit_shortnames[flavor])
                importlib.reload(settings)
                target_from_pkl = settings.context.load('train_target')
                target = data.pop(settings.target_column_name).to_numpy()
                target = target.reshape(-1, 1)
                self.assertIsNone(np.testing.assert_array_equal(target_from_pkl, target))


class TestIOReadCSVClaustering(Base):
    """
    This class performs unittests for the pre processing flavors that utilize regression data
    """
    category = 'clustering'
    @parameterized.expand(tests_io_read_csv_clustering)
    def test_correct_data_is_stored(self, flavor):
        import settings
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])
        data = pandas.read_csv(settings.datafile)
        for do_predict in [False, True]:
            if do_predict:
                self.set_to_predict_phase()
                os.system('python ' + unit_shortnames[flavor])
                importlib.reload(settings)
                descriptors_from_pkl = settings.context.load('descriptors')
                descriptors = data.to_numpy()
                self.assertIsNone(np.testing.assert_array_equal(descriptors_from_pkl, descriptors))
            else:
                os.system('python ' + unit_shortnames[flavor])
                importlib.reload(settings)
                target_from_pkl = settings.context.load('train_target')
                target = data.to_numpy()[:, 0]
                target = target.reshape(-1, 1)
                self.assertIsNone(np.testing.assert_array_equal(target_from_pkl, target))


class TestPreProcessingRegression(Base):
    """
    This class performs unittests for the pre processing flavors that utilize regression data
    """

    category = 'regression'

    @parameterized.expand(tests_pre_processing_regression)
    def test_flavor(self, flavor):

        # We first have to import settings
        import settings

        # Copy flavor from assets
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])

        # This test does not use pickles; it generates the needed pickles files
        # Make a pandas data frame with data formed during setUp in base class
        data = pandas.read_csv('data_to_train_with.csv')

        # Get target and descriptors after custom manipulation of the data
        target = data.pop(settings.target_column_name).to_numpy()
        target = target.reshape(-1, 1)  # Reshape array from a row vector into a column vector
        descriptors = data.to_numpy()

        # Save data as a pickle in .job_context using context object

        # Save target and descriptors in the 'context_paths' dictionary
        context = settings.Context()
        context.save(target, 'train_target')
        context.save(descriptors, 'train_descriptors')
        context.save(target, 'test_target')
        context.save(descriptors, 'test_descriptors')

        # Run flavor - this write the (now) 'pre processed' data to .job_content
        os.system('python '+ unit_shortnames[flavor])

        # Load the (hopefully) modified data in .job_context
        train_target = context.load("train_target")
        train_descriptors = context.load("train_descriptors")
        test_target = context.load("test_target")
        test_descriptors = context.load("test_descriptors")

        # Check the pass conditions for each data loaded
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


class TestModelRegression(Base):
    """
    This class performs unittests for the model flavors in the 'regression' category
    """

    category = 'regression'

    @parameterized.expand(tests_model_regression)
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
            else:
                # Assertions to be made after training
                os.system('python '+ unit_shortnames[flavor])
                assert(os.path.isfile(os.path.join('.job_context', 'RMSE.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'train_predictions.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_predictions.pkl')))


class TestModelClassification(Base):
    """
    This class performs unittests for the model flavors in the 'classification' category
    """

    category = 'classification'

    @parameterized.expand(tests_model_classification)
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
            else:
                # Assertions to be made after training
                os.system('python '+ unit_shortnames[flavor])
                assert (os.path.isfile(os.path.join('.job_context', 'test_probabilities.pkl')))
                assert (os.path.isfile(os.path.join('.job_context', 'confusion_matrix.pkl')))
                assert (os.path.isfile(os.path.join('.job_context', 'train_predictions.pkl')))
                assert (os.path.isfile(os.path.join('.job_context', 'test_predictions.pkl')))


class TestModelClustering(Base):
    """
    This class performs unittests for the model flavors in the 'clustering' category
    """

    category = 'clustering'

    @parameterized.expand(tests_model_clustering)
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
            else:
                # Assertions to be made after training
                os.system('python '+ unit_shortnames[flavor])
                assert(os.path.isfile(os.path.join('.job_context', 'train_labels.pkl')))
                assert(os.path.isfile(os.path.join('.job_context', 'test_labels.pkl')))


class TestPostProcessingRegression(Base):
    """
    This class performs unittests for the flavors in the 'post processing' category
    """

    category = 'regression'

    @parameterized.expand(tests_post_processing_regression)
    def test_flavor(self, flavor):
        # copy flavor
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])
        import settings
        with settings.context as context:
            context.context_paths.update({'train_predictions': 'fixtures/regression_pkls/train_predictions.pkl',
                                            'test_predictions': 'fixtures/regression_pkls/test_predictions.pkl',})
        os.system('python ' + unit_shortnames[flavor])
        assert(os.path.isfile('my_parity_plot.png'))


class TestPostProcessingClassification(Base):
    """
    This class performs unittests for the flavors in the 'post processing' category
    """

    category = 'classification'

    @parameterized.expand(tests_post_processing_classification)
    def test_flavor(self, flavor):
        # copy flavor
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])
        import settings
        with settings.context as context:
            context.context_paths.update({'test_target': 'fixtures/classification_pkls/test_target.pkl',
                                          'test_probabilities': 'fixtures/classification_pkls/test_probabilities.pkl', })
        os.system('python ' + unit_shortnames[flavor])
        assert (os.path.isfile('my_roc_curve.png'))


class TestPostProcessingClustering(Base):
    """
    This class performs unittests for the flavors in the 'post processing' category
    """

    category = 'clustering'

    @parameterized.expand(tests_post_processing_clustering)
    def test_flavor(self, flavor):
        # copy flavor
        shutil.copy(asset_path + unit_shortnames[flavor], unit_shortnames[flavor])
        import settings
        with settings.context as context:
            context.context_paths.update({'train_labels': 'fixtures/clustering_pkls/train_labels.pkl',
                                          'test_labels': 'fixtures/clustering_pkls/test_labels.pkl',
                                          'train_descriptors': 'fixtures/clustering_pkls/train_descriptors.pkl',
                                          'test_descriptors': 'fixtures/clustering_pkls/test_descriptors.pkl',
                                          'descriptor_scaler': 'fixtures/clustering_pkls/descriptor_scaler.pkl', })
        os.system('python ' + unit_shortnames[flavor])
        assert (os.path.isfile('train_test_split.png'))
        assert (os.path.isfile('test_clusters.png'))


if __name__ == '__main__':
    unittest.main()
