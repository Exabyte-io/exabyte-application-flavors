#!/usr/bin/env python
import os
import shutil
import unittest
import subprocess
from parameterized import parameterized
from unittest_baseclass import BaseUnitTest


class TestPostProcessingFlavors(BaseUnitTest):
    """
    This class performs unit tests for the post-processing flavors
    """

    def run_flavor_test(self, category, flavor, plots):
        """
        This function runs each flavor test whether in training or predict mode.

        Args:
            category (str): the problem category
                Ex) 'regression', 'classification', 'clustering'
            flavor (str): name of the python model flavor file in assets
            plots (str): name of the plot that is made by the flavor, and it is for
                this plot we check
        """
        self.set_pickle_fixtures_path_in_context_object(category, 'model_data')
        shutil.copy(os.path.join(self.asset_path, flavor), flavor)
        subprocess.call(['python', flavor])
        for plot in plots:
            assert os.path.isfile(plot)

    params = [
        ['regression', 'pyml:post_processing:parity_plot:matplotlib.pyi', ['my_parity_plot.png']],
        ['classification', 'pyml:post_processing:roc_curve:sklearn.pyi', ['my_roc_curve.png']],
        ['clustering', 'pyml:post_processing:pca_2d_clusters:matplotlib.pyi', ['train_test_split.png',
                                                                               'train_clusters.png',
                                                                               'test_clusters.png']],
    ]

    @parameterized.expand(params)
    def test_post_processing_flavors(self, category, flavor, plots):
        self.custom_setup(category)
        self.run_flavor_test(category, flavor, plots)


if __name__ == '__main__':
    unittest.main()
