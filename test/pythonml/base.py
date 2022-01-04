import os
import sys
import yaml
import importlib
import subprocess as sp
from shutil import rmtree, copy
from tempfile import mkdtemp
from unittest import TestCase
from functools import lru_cache

from parameterized import parameterized


@lru_cache(maxsize=1)
def load_manifest():
    dirname = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(
        dirname, "integration_configuration.yaml"
    )
    with open(path, "r") as f:
        return yaml.safe_load(f)


class BaseTest(TestCase):
    subdir = "fixtures"
    asset_dir = "../../assets/python/ml"
    settings_basename = "settings.py"
    category = "regression"
    data_type = "scaled_data"
    needs_data = False

    @staticmethod
    def get_func_name(testcase_func, param_num, params):
        args, _ = params
        try:
            name = args[0]["name"]
        except (KeyError, TypeError):
            name = args[0]
        return "%s_%s_%s" % (
            testcase_func.__name__,
            parameterized.to_safe_name(name),
            param_num
        )

    @staticmethod
    def get_workflow_flavors(category: str):
        manifest = load_manifest()
        flavor_map = manifest["unit_shortnames"]
        flavors = [
            ({
                "name": name,
                "flavors": [
                    flavor_map[unit] for unit in test["units_to_run"]
                ],
                **test
            },) for name, test in manifest["tests"].items()
            if test["category"] == category
        ]
        return flavors

    @staticmethod
    def reload_settings():
        import settings
        importlib.reload(settings)
        return settings

    @staticmethod
    def run_process(flavor: str):
        proc = sp.Popen(
            (sys.executable, flavor), stdout=sp.PIPE, stderr=sp.PIPE
        )
        out, err = proc.communicate()
        if proc.returncode:
            raise Exception(f"out={out}, err={err}")

    def relpath(self, basename: str) -> str:
        dirname = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(dirname, self.subdir, basename)

    def tmppath(self, basename: str) -> str:
        return os.path.join(self.tmpdir, basename)

    def assetpath(self, basename: str) -> str:
        dirname = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(dirname, self.asset_dir, basename)

    def copy_asset(self, flavor: str):
        # This file is a Jinja template so copy a pre-rendered mock instead
        if flavor == "pyml:data_input:train_test_split:sklearn.pyi":
            copy(self.relpath("train_test_split.py"), self.tmppath(flavor))
        else:
            copy(self.assetpath(flavor), self.tmppath(flavor))

    def copy_data(self):
        """
        Copy data files into tmpdir for processing.
        """
        if self.category == "clustering":
            training_file = "clustering_blobs.csv"
            predict_file = "clustering_blobs.csv"
        else:
            training_file = f"{self.category}_training_data.csv"
            predict_file = f"{self.category}_predict_data.csv"
        copy(self.relpath(training_file), self.tmppath("data_to_train_with.csv"))
        copy(self.relpath(predict_file), self.tmppath("data_to_predict_with.csv"))

    def setUp(self):
        self.orig_dir = os.getcwd()
        self.tmpdir = mkdtemp()
        os.chdir(self.tmpdir)
        sys.path.insert(0, self.tmpdir)
        with open(self.relpath(self.settings_basename), 'r') as template, \
                open(self.tmppath(self.settings_basename), 'w') as settings:
            settings.write(
                template.read()
                    .replace("PROBLEM_CATEGORY_HERE", self.category)
                    .replace("BASE_DIR = None", f'BASE_DIR = "{self.tmpdir}"')
            )
        settings = self.reload_settings()
        self.context = settings.Context()
        if self.needs_data:
            self.copy_data()

    def tearDown(self):
        del sys.modules["settings"]
        sys.path.remove(self.tmpdir)
        rmtree(self.tmpdir)
        os.chdir(self.orig_dir)

