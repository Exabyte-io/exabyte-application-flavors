#!/usr/bin/env python

import os
import sys
import unittest
import shutil
import subprocess
from fixtures.settings import Context
import pandas as pd
import numpy as np
np.random.seed(0)

flavor_file = 'pyml:pre_processing:remove_missing:pandas.pyi'
settings_file = 'settings.py'


class TestRemoveMissing(unittest.TestCase):
    """
    This test tests the flavor pyml:pre_processing:remove_missing:pandas.pyi
    """

    def setUp(self):

        self.context = Context()

        # Make a pandas data frame with fake data
        self.fake_data = pd.DataFrame(np.random.randn(5, 5), columns=['a', 'b', 'c', 'd', 'target'])

        # Edit the fake data to be useful for this test. Insert 'np.nan' and bottom left and top right
        self.fake_data.loc[4,'a'] = np.nan
        self.fake_data.loc[0,'target'] = np.nan

        # From the fake data, get the target col
        self.fake_data_target = self.fake_data.iloc[:, -1]
        self.fake_data_descriptors = self.fake_data.iloc[:, :-1]

        # save fake_data as a pickle in .job_context using context
        self.context.save(self.fake_data_target, 'train_target')
        self.context.save(self.fake_data_descriptors, 'train_descriptors')
        self.context.save(self.fake_data_target, 'test_target')
        self.context.save(self.fake_data_descriptors, 'test_descriptors')

        # copy in the needed files for the test and assert they are indeed here
        shutil.copy(os.path.join('../../assets/python/ml/', flavor_file), '.')
        shutil.copy(os.path.join('fixtures', settings_file), '.')
        assert(os.path.isfile(flavor_file))
        assert(os.path.isfile(settings_file))

        # run the flavor
        pipes = subprocess.Popen((sys.executable, flavor_file), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pipes.communicate()

    def tearDown(self):
        os.system('rm -rf .job_context')
        os.system('rm -rf pyml*')

    def test_pkl_files_exist(self):
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'train_target.pkl')))
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'test_descriptors.pkl')))
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'train_target.pkl')))
        assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'test_descriptors.pkl')))

    def test_duplicates_removed_from_training_set(self):
        # load the (hopefully) modified data
        train_target = self.context.load("train_target")
        train_descriptors = self.context.load("train_descriptors")
        test_target = self.context.load("test_target")
        test_descriptors = self.context.load("test_descriptors")

        # turn the data into data frames
        train_target_df = pd.DataFrame(train_target)
        train_descriptors_df = pd.DataFrame(train_descriptors)
        test_target_df = pd.DataFrame(test_target)
        test_descriptors_df = pd.DataFrame(test_descriptors)

        # assert that the data frames have met the test condition
        self.assertFalse(train_target_df.isnull().values.any())
        self.assertFalse(train_descriptors_df.isnull().values.any())
        self.assertFalse(test_target_df.isnull().values.any())
        self.assertFalse(test_descriptors_df.isnull().values.any())


if __name__ == '__main__':
    unittest.main()
