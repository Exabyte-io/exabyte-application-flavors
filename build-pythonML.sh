#!/bin/bash

CURRENT_DIR=$( pwd )
BASE_DIR=$(dirname "$0")
PYTHON_ASSETS_PATH="assets/python"
PATH_TO_PYTHON_TREE="src/js/python"

cd $PYTHON_ASSETS_PATH
python "build_tree.py" $PATH_TO_PYTHON_TREE -b $BASE_DIR
cd $CURRENT_DIR
