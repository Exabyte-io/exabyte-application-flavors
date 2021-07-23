#!/usr/bin/env python
import os
import re
import unittest
import subprocess
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

    def tearDown(self):
        for data in ['.job_context', 'settings.py']:
            subprocess.call('rm -rf '+data, shell=True)

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('pickle.dump')
    def test_update_context(self, mock_pickle, mock_builtin_open):
        """
        This function update_content is supposed to pickle .job_context/workflow_context_file_mapping as the key
        _context_file. We check this by seeing if mock open is called with (self.context._context_file, "wb").
        Then, we see if pickle dump is actually dumping the correct mock object
        """
        self.context._update_context()
        builtin_open_calls = [mock.call(self.context._context_file, "wb")]
        mock_builtin_open.assert_has_calls(builtin_open_calls)
        mock_pickle_calls = [mock.call(self.context.context_paths, mock_builtin_open())]
        mock_pickle.assert_has_calls(mock_pickle_calls)

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('pickle.dump')
    def test_save(self, mock_pickle, mock_builtin_open):
        """
        The context_paths variable contains the key value pairs of the pickled files.
        The save function pickles a file and saves it in the .job_context directory

        To test this, we first make a object, obj, in order to be able to call the save function.
        The mock open will return a mock object. This is what would normally be the path of
        where the object will be pickled. We assert that pickle dump pickles our object, obj,
        to the correct path by asserting it pickles obj with the mock open object
        """
        obj = object()
        self.context.save(obj, 'fake_obj')
        builtin_open_calls = [mock.call(os.path.join(self.context._context_dir_pathname, f"fake_obj.pkl"), "wb")]
        mock_builtin_open.assert_has_calls(builtin_open_calls)
        mock_pickle_calls = [mock.call(obj, mock_builtin_open())]
        mock_pickle.assert_has_calls(mock_pickle_calls)
        self.context.context_paths.pop('fake_obj', None)

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('pickle.load')
    def test_load(self, mock_pickle, mock_builtin_open):
        """
        The load function return an object that has been pickled and stored in the
        .job_context folder. It knows which pickled object to get by using a 'name'
        parameter

        To test this function, we first set a path to a fake pickled object. Then, we pass
        the key to the fake pickled object to load. When load is called, we have to assert
        that the mock open object will be trying to open the fake pickled object.
        We want the mock open object to be what is loaded by pickle, and we want what is
        returned by mock pickle to be what is returned by load
        """
        self.context.context_paths.update({'key_of_fake_obj': '.job_context/fake_obj.pkl'})
        obj = self.context.load('key_of_fake_obj')
        builtin_open_calls = [mock.call('.job_context/fake_obj.pkl', "rb")]
        mock_builtin_open.assert_has_calls(builtin_open_calls)
        mock_pickle_calls = [mock.call(mock_builtin_open())]
        mock_pickle.assert_has_calls(mock_pickle_calls)
        assert mock_pickle() == obj


if __name__ == '__main__':
    unittest.main()
