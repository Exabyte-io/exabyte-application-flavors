#!/usr/bin/env python

from fixtures.unittest_utils import setup_model_flavor
from parameterized import parameterized
import os
import unittest


class TestRegressionFlavors(unittest.TestCase):
    """
    This class performs unittests for the flavors in the 'regression' category
    """

    category = 'regression'

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
        [{'flavor_file': 'pyml:model:gradboosted_trees_regression:sklearn.pyi',
          'model_pickle_file': 'gradboosted_tree_regression.pkl'}],

        [{'flavor_file': 'pyml:model:extreme_gradboosted_trees_regression:sklearn.pyi',
          'model_pickle_file': 'extreme_gradboosted_tree_regression.pkl'}],

        [{'flavor_file': 'pyml:model:bagged_trees_regression:sklearn.pyi',
          'model_pickle_file': 'bagged_trees_regression.pkl'}],

        [{'flavor_file': 'pyml:model:adaboosted_trees_regression:sklearn.pyi',
          'model_pickle_file': 'adaboosted_tree_regression.pkl'}],

        [{'flavor_file': 'pyml:model:kernel_ridge_regression:sklearn.pyi',
          'model_pickle_file': 'kernel_ridge_regression.pkl'}],

        [{'flavor_file': 'pyml:model:lasso_regression:sklearn.pyi',
          'model_pickle_file': 'lasso_regression.pkl'}],

        [{'flavor_file': 'pyml:model:random_forest_regression:sklearn.pyi',
          'model_pickle_file': 'random_forest_regression.pkl'}],

        [{'flavor_file': 'pyml:model:ridge_regression:sklearn.pyi',
          'model_pickle_file': 'ridge_regression.pkl'}],

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
                # Assertions to be made after training
                assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, params['model_pickle_file'])))
                assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'RMSE.pkl')))
                assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'train_target.pkl')))
                assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'target_scaler.pkl')))


if __name__ == '__main__':
    unittest.main()
