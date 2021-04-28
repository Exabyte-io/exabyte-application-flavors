#!/usr/bin/env python
"""
Build script to generate an assets.js and tree.js file for Python sources
to the file specified in stdin.
"""
import os, sys, subprocess
from typing import List, Dict
import argparse
import yaml

# Set up argparse for the script. Currently just takes in a single argument, for the output script.
# Todo: Should we have these build tools to /src, and have the resultant Python/JS packages exist in /build instead?
parser = argparse.ArgumentParser(
    description="Configuration script un by `build-pythonML.sh` in the parent dir. Don't run this directly."
)
parser.add_argument('relative_sources_path', type=str, nargs=1,
                    help="Path to the Python folder of the JS package")
parser.add_argument('-b', '--base_dir', metavar="base_dir", type=str, nargs=1,
                    help="Base directory of the package")
args = parser.parse_args()
relative_sources_path: str = args.relative_sources_path.pop()
base_dir: str = args.base_dir.pop()

# Determine where to output the build files
output_path = os.path.join(base_dir, relative_sources_path)
current_dir = os.path.dirname(__file__)

# Read in the main manifest
with open(os.path.join(current_dir, "manifest.yaml"), "r") as inp:
    main_manifest = yaml.safe_load(inp)


class Config(object):
    def __init__(self, flavor_list_display_name: str, true_extension: str, source_filename: str,
                 application_dirname: str,
                 context_providers: List[str] = None, flavor_list_template_name: str = None,
                 inputs: List[Dict[str, str]] = None):
        self.flavorListDisplayName = flavor_list_display_name
        self.trueExtension = true_extension
        self.sourceFilename = source_filename
        self.application_dirname = application_dirname

        if flavor_list_template_name is None:
            self.flavorListTemplateName = flavor_list_display_name + true_extension
        else:
            self.flavorListTemplateName = flavor_list_template_name

        # Using None as a sentry value to avoid setting the empty list as a default arg, since we don't want the same
        # list instance shared by all members of this class.
        if context_providers is None:
            self.contextProviders = []
        else:
            self.contextProviders = context_providers

        if inputs is None:
            self.inputs = []
        else:
            self.inputs = inputs

    @classmethod
    def from_config_and_manifest(cls, path: str, flavor: Dict[str, str]):
        result = None

        if path.startswith("."):
            # General python scripts are found in this section. Many of the are a bit old,
            # so the naming convention between the name in assets/tree isn't entirely consistent
            # ToDo: Rename the names to allow us to remove this branching behavior
            flavor_list_display_name = flavor["flavor_list_display_name"]
            true_extension = flavor["true_extension"]
            source_filename = flavor["source_filename"]
            application_dirname = "python"

            if "extra_inputs" in flavor:
                inputs = [{
                    "name": flavor['extra_inputs'],
                    "templateName": flavor['extra_inputs']
                }]
            else:
                inputs = None

            result = cls(flavor_list_display_name,
                         true_extension,
                         source_filename,
                         application_dirname,
                         inputs=inputs)

        elif path.startswith("ml"):
            # Machine learning scripts here.
            flavor_list_display_name = ""
            true_extension = ""
            source_filename = ""
            application_dirname = "python/ml"

            if "extra_inputs" in flavor:
                inputs = [{
                    "name": flavor['extra_inputs'],
                    "templateName": flavor['extra_inputs']
                }]
            else:
                inputs = None

            result = cls(flavor_list_display_name,
                         true_extension,
                         source_filename,
                         application_dirname,
                         inputs=inputs)


        if result is None:
            raise NotImplementedError(f"The path {path} has not been configured for automatic configuration yet.")

        return result


# Figure out where our other manifests are
manifest_paths = []
for directory, manifests in main_manifest.items():
    if directory == "refactor_into_its_own_directory":
        directory = "."
    for manifest in manifests:
        path_to_manifest = os.path.join(directory, manifest)
        manifest_paths.append(path_to_manifest)

# Write the assets files
configs = []
for path in manifest_paths:
    with open(path, "r") as inp:
        flavors = list(yaml.safe_load_all(inp))
        for flavor in flavors:
            Config.from_config_and_manifest(path, flavor)
