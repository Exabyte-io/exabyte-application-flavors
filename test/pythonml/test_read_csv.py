#!/usr/bin/env python

from fixtures.unittest_utils import setup_settings
from parameterized import parameterized
import os
import sys
import shutil
import unittest
import importlib
import subprocess
import pandas as pd
import numpy as np


flavor_file = 'pyml:data_input:read_csv:pandas.pyi'
settings_file = 'settings.py'


class TestReadCSV(unittest.TestCase):
    """
    Unit tests for the methods in the Context class defined in the settings.py module
    """

    def setup(self, category, do_predict=False):
        """
        This is a custom setup function, not unittest's 'setUp'
        """

        # Set up the settings.py needed here. Since we make a new file for import each time
        # we should reload it
        setup_settings(category, do_predict)
        import settings
        importlib.reload(settings)

        # copy in additional needed files for the test and assert all needed files are here
        if category == 'clustering':
            copy_file = "clustering_blobs.csv"
        else:
            if do_predict:
                copy_file = "{category}_{run_type}_data.csv".format(category=category, run_type='predict')
            else:
                copy_file = "{category}_{run_type}_data.csv".format(category=category, run_type='training')

        # copy all additional needed files and asserts all needed files are here
        shutil.copy(os.path.join('fixtures', copy_file), '.')
        shutil.copy(os.path.join('../../assets/python/ml/', flavor_file), '.')
        assert(os.path.isfile(flavor_file))
        assert(os.path.isfile(settings_file))
        assert(os.path.isfile(settings.datafile))

        # run the flavor
        pipes = subprocess.Popen((sys.executable, flavor_file), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = pipes.communicate()
        sys.stdout.write(stdout.decode())
        self.assertFalse(stderr, f"\nSTDERR:\n{stderr.decode()}")

        # make a context object and get some properties from settings.py
        self.context = settings.Context()
        self.datafile = settings.datafile
        self.target_column_name = settings.target_column_name

    def tearDown(self):
        os.system('rm -rf .job_context')
        os.system('rm -rf pyml*')
        os.system('rm -rf settings.py')
        os.system('rm -rf *.csv')

    @parameterized.expand([
        ['regression', False],
        ['regression', True],
        ['classification', False],
        ['classification', True],
        ['clustering', False],
        ['clustering', True],
    ])
    def test_if_correct_pickles_generated(self, category, do_predict):
        self.setup(category, do_predict)
        if do_predict:
            assert (os.path.isfile(os.path.join(self.context._context_dir_pathname, 'descriptors.pkl')))
        else:
            assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'train_target.pkl')))
            assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'test_descriptors.pkl')))
            assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'train_target.pkl')))
            assert(os.path.isfile(os.path.join(self.context._context_dir_pathname, 'test_descriptors.pkl')))
        self.tearDown()

    @parameterized.expand([
        ['regression', False],
        ['regression', True],
        ['classification', False],
        ['classification', True],
        ['clustering', False],
        ['clustering', True],
    ])
    def test_pickled_targets_correct(self, category, do_predict):
        self.setup(category, do_predict)
        data = pd.read_csv(self.datafile)
        if do_predict:
            descriptors_from_pkl = self.context.load('descriptors')
            descriptors = data.to_numpy()
            self.assertIsNone(np.testing.assert_array_equal(descriptors_from_pkl, descriptors))
        else:
            target_from_pkl = self.context.load('train_target')
            if category == 'clustering':
                target = data.to_numpy()[:, 0]
            else:
                target = data.pop(self.target_column_name).to_numpy()
            if category == 'classification':
                target = target.astype(int)
            target = target.reshape(-1, 1)
            self.assertIsNone(np.testing.assert_array_equal(target_from_pkl, target))
        self.tearDown()


if __name__ == '__main__':
    unittest.main()
