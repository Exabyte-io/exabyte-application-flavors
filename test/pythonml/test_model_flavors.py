#!/usr/bin/env python
import importlib
import os
import shutil
import unittest
import subprocess
from parameterized import parameterized
from unittest_baseclass import BaseUnitTest


class TestModelFlavors(BaseUnitTest):
    """
    This class performs unit tests for the model flavors
    """

    @staticmethod
    def assert_pass_conditions_training(category):
        """
        This function asserts pass condition for the model flavors during the training phase

        Args:
            category (str): the problem category
                Ex) 'regression', 'classification', etc
        """
        # import settings and reload it - this makes the context paths dicitonary in the context object
        import settings
        importlib.reload(settings)
        with settings.context as context:
            if category == 'regression':
                rmse = context.load('RMSE')
                rmse_cutoff = 20
                assert rmse <= rmse_cutoff
            elif category == 'classification':
                confusion_matrix = context.load('confusion_matrix')
                accuracy = confusion_matrix.diagonal() / confusion_matrix.sum(axis=0)
                accuracy_cutoff = 0.6
                assert accuracy.all() >= accuracy_cutoff

    @staticmethod
    def assert_pass_conditions_predicting():
        assert os.path.isfile('predictions.csv')

    def run_flavor_test(self, category, flavor, is_predicting):
        """
        This function runs each flavor test whether in training or predict mode.

        Args:
            category (str): the problem category
                Ex) 'regression', 'classification', 'clustering'
            flavor (str): name of the python model flavor file in assets
            is_predicting (Boolean): True if we are making a prediction, False if
                we are training
        """
        self.set_pickle_fixtures_path_in_context_object(category, 'scaled_data')
        shutil.copy(os.path.join(self.asset_path, flavor), flavor)
        if is_predicting:
            self.set_to_predict_phase()
            subprocess.call(['python', flavor])
            self.assert_pass_conditions_predicting()
        else:
            subprocess.call(['python', flavor])
            self.assert_pass_conditions_training(category)

    params = [
        ['regression', 'pyml:model:adaboosted_trees_regression:sklearn.pyi'],
        ['regression', 'pyml:model:bagged_trees_regression:sklearn.pyi'],
        ['regression', 'pyml:model:gradboosted_trees_regression:sklearn.pyi'],
        ['regression', 'pyml:model:extreme_gradboosted_trees_regression:sklearn.pyi'],
        ['regression', 'pyml:model:kernel_ridge_regression:sklearn.pyi'],
        ['regression', 'pyml:model:lasso_regression:sklearn.pyi'],
        ['regression', 'pyml:model:multilayer_perceptron_regression:sklearn.pyi'],
        ['regression', 'pyml:model:random_forest_regression:sklearn.pyi'],
        ['regression', 'pyml:model:ridge_regression:sklearn.pyi'],
        ['classification', "pyml:model:random_forest_classification:sklearn.pyi"],
        ['classification', "pyml:model:gradboosted_trees_classification:sklearn.pyi"],
        ['classification', "pyml:model:extreme_gradboosted_trees_classification:sklearn.pyi"],
        ['clustering', "pyml:model:k_means_clustering:sklearn.pyi"],
    ]

    @parameterized.expand(params)
    def test_flavor(self, category, flavor):
        self.custom_setup(category)
        self.run_flavor_test(category, flavor, is_predicting=False)
        self.run_flavor_test(category, flavor, is_predicting=True)


if __name__ == '__main__':
    unittest.main()
