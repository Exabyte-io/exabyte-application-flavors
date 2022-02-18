#!/usr/bin/env python
from parameterized import parameterized

from flavor import BaseFlavorTest


class TestClusteringFlavors(BaseFlavorTest):
    # TODO : we don't actually verify anything for clustering
    category = "clustering"
    plot_name = "train_clusters.png"
    plot_unit = "POS_plotClust"

    @parameterized.expand(
        BaseFlavorTest.get_workflow_flavors(category),
        name_func=BaseFlavorTest.get_func_name,
    )
    def test_workflows(self, test_params):
        self.run_workflow(test_params)

    flavors = [
        ("pyml:model:k_means_clustering:sklearn.pyi",),
        (
            "pyml:post_processing:pca_2d_clusters:matplotlib.pyi",
            {"pngs": ["train_test_split.png", "train_clusters.png", "test_clusters.png"]},
        ),
    ]

    @parameterized.expand(
        flavors,
        name_func=BaseFlavorTest.get_func_name,
    )
    def test_flavors(self, flavor, kws=None):
        self.run_flavor(flavor, kws)
