#!/usr/bin/env python

import os
import re
import unittest
from unittest import mock


class TestContext(unittest.TestCase):
    """
    Unit tests for the methods in the Context class defined in the settings.py module
    """

    def setUp(self):
        with open('fixtures/settings.py', 'r') as file:
            unmodified_settings_file = file.readlines()
        with open('settings.py', 'w') as file:
            for line in unmodified_settings_file:
                line = re.sub("PROBLEM_CATEGORY_HERE", 'regression', line)
                file.write(line)
        import settings
        self.context = settings.Context()
        self.context.context_paths.update({self.context._context_file: 'file'})

    def tearDown(self):
        os.system('rm -rf .job_context')
        os.system('rm settings.py')

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('pickle.dump')
    def test_update_context(self, mock_pickle, mock_builtin_open):
        self.context._update_context()
        builtin_open_calls = [mock.call(self.context._context_file, "wb")]
        mock_builtin_open.assert_has_calls(builtin_open_calls)
        mock_pickle_calls = [mock.call(self.context.context_paths, mock_builtin_open())]
        mock_pickle.assert_has_calls(mock_pickle_calls)

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('pickle.dump')
    def test_save(self, mock_pickle, mock_builtin_open):
        obj = object()
        self.context.save(obj, 'fake_name')
        builtin_open_calls = [mock.call(os.path.join(self.context._context_dir_pathname, f"fake_name.pkl"), "wb")]
        mock_builtin_open.assert_has_calls(builtin_open_calls)
        mock_pickle_calls = [mock.call(obj, mock_builtin_open())]
        mock_pickle.assert_has_calls(mock_pickle_calls)
        self.context.context_paths.pop('fake_name', None)

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('pickle.load')
    def test_load(self, mock_pickle, mock_builtin_open):
        self.context.load(self.context._context_file)
        builtin_open_calls = [mock.call('file', "rb")]
        mock_builtin_open.assert_has_calls(builtin_open_calls)
        mock_pickle_calls = [mock.call(mock_builtin_open())]
        mock_pickle.assert_has_calls(mock_pickle_calls)


if __name__ == '__main__':
    unittest.main()
