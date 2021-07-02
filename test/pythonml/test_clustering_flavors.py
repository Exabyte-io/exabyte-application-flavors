#!/usr/bin/env python

from fixtures.unittest_utils import setup_model_flavor
from parameterized import parameterized
import os
import unittest


class TestClusteringFlavors(unittest.TestCase):
    """
    This class performs unittests for the flavors in the 'clustering' category
    """

    category = 'clustering'

    @staticmethod
    def teardown():
        """
        A custom tear down class to be called after each time we test a flavor
        using 'prediction' instead of 'training'.
        """
        os.system('rm -rf .job_context')
        os.system('rm -rf pyml*')
        os.system('rm settings.py')
        #os.system('rm *.csv')

    @parameterized.expand([
        [{'flavor_file': 'pyml:model:k_means_clustering:sklearn.pyi'}],
    ])
    def test_flavor(self, params):
        params.update({'settings_file': 'settings.py'})
        # False should come before true because we are to train before predict
        for do_predict in [False, True]:
            setup_model_flavor(self, self.category, do_predict, params)
            if do_predict:
                # Assertions to be made after predicting
                assert(os.path.isfile('predictions.csv'))
                self.teardown()
            else:
                # Assertions to be made after training
                assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'train_labels.pkl')))
                assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'test_labels.pkl')))


if __name__ == '__main__':
    unittest.main()
