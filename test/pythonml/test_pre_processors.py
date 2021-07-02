#!/usr/bin/env python

from fixtures.unittest_utils import setup_pre_processing_flavor, pre_processor_pass_conditions
from parameterized import parameterized
import os
import unittest
import numpy as np


class TestPreProcessors(unittest.TestCase):
    """
    This test tests the flavor pyml:pre_processing:remove_missing:pandas.pyi
    """

    def tearDown(self):
        os.system('rm -rf .job_context')
        os.system('rm -rf pyml*')
        os.system('rm *settings*')

    @parameterized.expand([
        [{'flavor_file': 'pyml:pre_processing:min_max_scaler:sklearn.pyi'}],
        [{'flavor_file': 'pyml:pre_processing:standardization:sklearn.pyi'}],
        [{'flavor_file': 'pyml:pre_processing:remove_duplicates:pandas.pyi'}],
        [{'flavor_file': 'pyml:pre_processing:remove_missing:pandas.pyi'}],
    ])
    def test_flavor(self, params):

        params.update({'settings_file': 'settings.py'})
        # Here, we just pass regression as a dummy variable
        setup_pre_processing_flavor(self, params)

        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'train_target.pkl')))
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'test_descriptors.pkl')))
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'train_target.pkl')))
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'test_descriptors.pkl')))
        if 'sklearn' in params['flavor_file']:
            assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'target_scaler.pkl')))
            assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'descriptor_scaler.pkl')))

        # check pass condition for the flavor of intrest
        pre_processor_pass_conditions(self, params)

if __name__ == '__main__':
    unittest.main()
