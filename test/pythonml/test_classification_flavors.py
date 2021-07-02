#!/usr/bin/env python

from fixtures.unittest_utils import setup_model_flavor
from parameterized import parameterized
import os
import unittest


class TestClassification(unittest.TestCase):
    """
    This test tests the flavor pyml:pre_processing:remove_missing:pandas.pyi
    """

    category = 'classification'

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

    @parameterized.expand([
        [{'flavor_file': 'pyml:model:gradboosted_trees_classification:sklearn.pyi',
          'model_pickle_file': 'gradboosted_trees_classification.pkl'}],

        [{'flavor_file': 'pyml:model:extreme_gradboosted_trees_classification:sklearn.pyi',
          'model_pickle_file': 'extreme_gradboosted_tree_classification.pkl'}],

        [{'flavor_file': 'pyml:model:random_forest_classification:sklearn.pyi',
          'model_pickle_file': 'random_forest_classification.pkl'}],

    ])
    def test_flavor(self, params):
        params.update({'settings_file': 'settings.py'})
        # False should come before true because we are to train before predict. The True / False in
        # parameterize refer to whether or not we shall predict
        for do_predict in [False, True]:
            setup_model_flavor(self, self.category, do_predict, params)
            if do_predict:
                # Assertions to be made after predicting
                assert(os.path.isfile('predictions.csv'))
                self.teardown()
            else:
                # tests for when training
                assert (os.path.isfile(os.path.join(self.context._context_dir_pathname, params['model_pickle_file'])))
                assert (os.path.isfile(os.path.join(self.context._context_dir_pathname, 'test_probabilities.pkl')))
                assert (os.path.isfile(os.path.join(self.context._context_dir_pathname, 'confusion_matrix.pkl')))
                assert (os.path.isfile(os.path.join(self.context._context_dir_pathname, 'train_predictions.pkl')))
                assert (os.path.isfile(os.path.join(self.context._context_dir_pathname, 'test_predictions.pkl')))


if __name__ == '__main__':
    unittest.main()
