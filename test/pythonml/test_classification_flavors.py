#!/usr/bin/env python
from parameterized import parameterized

from flavor import BaseFlavorTest


class TestClassificationFlavors(BaseFlavorTest):
    category = "classification"
    plot_name = "my_roc_curve.png"
    plot_unit = "POS_plotROC"

    @parameterized.expand(
        BaseFlavorTest.get_workflow_flavors(category),
        name_func=BaseFlavorTest.get_func_name
    )
    def test_workflows(self, test_params):
        self.run_workflow(test_params)

    flavors = [
        ("pyml:model:random_forest_classification:sklearn.pyi",),
        ("pyml:model:gradboosted_trees_classification:sklearn.pyi",),
        ("pyml:model:extreme_gradboosted_trees_classification:sklearn.pyi",),
        ("pyml:post_processing:roc_curve:sklearn.pyi", {"pngs": ["my_roc_curve.png"]}),
    ]

    @parameterized.expand(
        flavors,
        name_func=BaseFlavorTest.get_func_name,
    )
    def test_flavors(self, flavor, kws=None):
        self.run_flavor(flavor, kws)
