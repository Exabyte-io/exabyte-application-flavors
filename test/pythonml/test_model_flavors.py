#!/usr/bin/env python
import importlib
import os
import shutil
import unittest
from parameterized import parameterized
from fixtures.unittest_baseclass import BaseUnitTest



class TestModelFlavors(BaseUnitTest):
    """
    This class performs unit tests for the model flavors in the 'regression' category
    """

    def check_pass_conditions_training(self, category):
        import settings
        importlib.reload(settings)
        with settings.context as context:
            if category == 'regression':
                rmse = context.load('RMSE')
                assert(rmse <= 2 * 10)
            elif category == 'classification':
                confusion_matrix = context.load('confusion_matrix')
                accuracy = confusion_matrix.diagonal() / confusion_matrix.sum(axis=0)
                assert (accuracy.all() >= 0.6)

    def check_pass_conditions_predicting(self):
        assert (os.path.isfile('predictions.csv'))

    def run_flavor_test(self, category, flavor, do_predict):
        self.set_pickle_fixtures_path_in_context_object(category, 'scaled_data')
        shutil.copy(os.path.join(self.asset_path, flavor), flavor)
        if do_predict:
            self.set_to_predict_phase()
            os.system('python ' + flavor)
            self.check_pass_conditions_predicting()
        else:
            os.system('python ' + flavor)
            self.check_pass_conditions_training(category)

    params = [
        ['regression', 'pyml:model:adaboosted_trees_regression:sklearn.pyi'],
        ['regression', 'pyml:model:bagged_trees_regression:sklearn.pyi'],
        ['regression', 'pyml:model:gradboosted_trees_regression:sklearn.pyi'],
        ['regression', 'pyml:model:extreme_gradboosted_trees_regression:sklearn.pyi'],
        ['regression', 'pyml:model:kernel_ridge_regression:sklearn.pyi'],
        ['regression', 'pyml:model:lasso_regression:sklearn.pyi'],
        ['regression', 'pyml:model:multilayer_perceptron:sklearn.pyi'],
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
        self.run_flavor_test(category, flavor, do_predict=False)
        self.run_flavor_test(category, flavor, do_predict=True)

if __name__ == '__main__':
    unittest.main()
