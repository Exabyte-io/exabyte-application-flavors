#!/usr/bin/env python
from parameterized import parameterized

from flavor import BaseFlavorTest


class TestRegressionFlavors(BaseFlavorTest):
    category = "regression"
    plot_unit = "POS_plotParity"
    plot_name = "my_parity_plot.png"

    @parameterized.expand(
        BaseFlavorTest.get_workflow_flavors(category),
        name_func=BaseFlavorTest.get_func_name
    )
    def test_workflows(self, test_params):
        self.run_workflow(test_params)

    flavors = [
        ('pyml:pre_processing:min_max_scaler:sklearn.pyi',),
        ('pyml:model:adaboosted_trees_regression:sklearn.pyi',),
        ('pyml:model:bagged_trees_regression:sklearn.pyi',),
        ('pyml:model:gradboosted_trees_regression:sklearn.pyi',),
        ('pyml:model:extreme_gradboosted_trees_regression:sklearn.pyi',),
        ('pyml:model:kernel_ridge_regression:sklearn.pyi',),
        ('pyml:model:lasso_regression:sklearn.pyi',),
        ('pyml:model:multilayer_perceptron_regression:sklearn.pyi',),
        ('pyml:model:random_forest_regression:sklearn.pyi',),
        ('pyml:model:ridge_regression:sklearn.pyi',),
        ('pyml:pre_processing:min_max_scaler:sklearn.pyi',),
        ('pyml:pre_processing:standardization:sklearn.pyi',),
        ('pyml:pre_processing:remove_duplicates:pandas.pyi',),
        ('pyml:pre_processing:remove_missing:pandas.pyi',),
        ('pyml:post_processing:parity_plot:matplotlib.pyi', {"pngs": ['my_parity_plot.png']}),
    ]

    @parameterized.expand(
        flavors,
        name_func=BaseFlavorTest.get_func_name,
    )
    def test_flavors(self, flavor, kws=None):
        self.run_flavor(flavor, kws)
