#!/usr/bin/env python

import os
import re
import sys
import unittest
import shutil
import subprocess
from fixtures.settings import Context
import numpy as np
np.random.seed(0)


def setup_settings_regression():
    """
    A little function to setup a settings file that has category = 'regression'
    Args:
    Returns:
        None
    """
    with open('settings.py', 'r') as file:
        unmodified_settings_file = file.readlines()
    with open('settings.py', 'w') as file:
        for line in unmodified_settings_file:
            line = re.sub("PROBLEM_CATEGORY_HERE", 'regression', line)
            file.write(line)


flavor_file = 'pyml:pre_processing:standardization:sklearn.pyi'
settings_file = 'settings.py'


class TestStandardScaler(unittest.TestCase):
    """
    This test tests the flavor pyml:pre_processing:remove_missing:pandas.pyi
    """

    def setUp(self):

        self.context = Context()

        # Make a 5x5 np array with fake data
        self.fake_data = np.random.randn(5, 5)

        # From the fake data, get the target col and descriptors
        self.fake_data_target = self.fake_data[:, -1].reshape(-1, 1)
        self.fake_data_descriptors = self.fake_data[:, :-1]

        # save fake_data as a pickle in .job_context using context
        self.context.save(self.fake_data_target, 'train_target')
        self.context.save(self.fake_data_descriptors, 'train_descriptors')
        self.context.save(self.fake_data_target, 'test_target')
        self.context.save(self.fake_data_descriptors, 'test_descriptors')

        # copy in the needed files for the test and assert they are indeed here
        shutil.copy(os.path.join('../../assets/python/ml/', flavor_file), '.')
        shutil.copy(os.path.join('fixtures', settings_file), '.')
        setup_settings_regression()
        assert(os.path.isfile(flavor_file))
        assert(os.path.isfile(settings_file))

        # run the flavor
        pipes = subprocess.Popen((sys.executable, flavor_file), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pipes.communicate()

    def tearDown(self):
        os.system('rm -rf .job_context')
        os.system('rm -rf pyml*')
        os.system('rm *settings*')

    def test_pkl_files_exist(self):
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'train_target.pkl')))
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'test_descriptors.pkl')))
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'train_target.pkl')))
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'test_descriptors.pkl')))
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'target_scaler.pkl')))
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'descriptor_scaler.pkl')))

    def test_standard_scaler(self):
        # load the (hopefully) modified data
        train_target = self.context.load("train_target")
        train_descriptors = self.context.load("train_descriptors")
        test_target = self.context.load("test_target")
        test_descriptors = self.context.load("test_descriptors")

        # for each (hopefully) modified data, assert that the standard scaler condition is met
        # standard scaler condition: Columns have mean of 0 and standard_deviation of 1
        for fake_data_set in [train_target, train_descriptors, test_target, test_descriptors]:
            column_means = fake_data_set.mean(axis=0)
            column_standard_deviations = fake_data_set.std(axis=0)
            for column_mean in column_means:
                self.assertAlmostEqual(0.0, column_mean)
            for column_standard_deviation in column_standard_deviations:
                self.assertAlmostEqual(1.0, column_standard_deviation)


if __name__ == '__main__':
    unittest.main()
