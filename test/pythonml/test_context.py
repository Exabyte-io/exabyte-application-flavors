#!/usr/bin/env python

import os
import sys
import unittest
from unittest import mock
from fixtures.settings import Context

settings_file = 'settings.py'


class TestContext(unittest.TestCase):
    """
    Unit tests for the methods in the Context class defined in the settings.py module
    """

    def setUp(self):
        self.context = Context()
        self.context.context_paths.update({self.context._context_file: 'file.pkl'})

    def tearDown(self):
        os.system('rm -rf .job_context')

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
        builtin_open_calls = [mock.call('file.pkl', "rb")]
        mock_builtin_open.assert_has_calls(builtin_open_calls)
        mock_pickle_calls = [mock.call(mock_builtin_open())]
        mock_pickle.assert_has_calls(mock_pickle_calls)


if __name__ == '__main__':
    unittest.main()
