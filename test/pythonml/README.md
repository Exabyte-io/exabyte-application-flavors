# PythonML Unit Tests

This set of tests is configured using the `integration_configuration.yaml` file, which contains information for which
units are to be present in a test, and the order they're to be run in. It also contains general settings, such as where
the test fixtures are located, and which files need to be cleaned up when a test job is complete.

## Test Configuration

Tests are configured inside of the `integration_configuration.yaml` file. The following variables are defined therein:

### `asset_path`

Path to the folder where the python flavors are defined

### `fixtures`

An object with the following attributes:

- `path` - Path to the fixtures folder
- `settings` - Name of the pre-rendered settings file used by the test suite.

- Three variables, named `regression`, `classification`, and `clustering`. These handle configuration for the
  regression, classification, and clustering tests respectively. They each have the following two attributes:

    - `training_set_name` - Name of the training dataset for the particular problem category

    - `predict_set_name` - Name of the dataset to be used for test predictions

### `files_to_remove`

A list of files and directories to be removed at the end of every test

### `extensions_to_remove`

A list of file extensions, and any file with these extensions will be removed at the end of every test

### `unit_shortnames`

For convenience, we shorten the names of the flavors a bit to aid in defining the tests. For example, we might call "
pyml:data_input:read_csv:pandas.j2.py" instead "IO_readCSV" for brevity. The shortnames are organized by category. See
commentary in this section of the YAML file for more information.

### `tests`

This section is where the test configurations are actually defined. Each test must have a unique name, and is generally
named after the units contained in it. The `category` attribute describes the type of problem it performs: regression,
classification, or clustering. The `units_to_run` list contains, in orde, the units that will be run during the
workflow.

## Creating New Tests

To create a new test, add a new entry to the `tests` variable in `integration_configuration.yaml`. The name of the test
should be unique. It must have a category, and at least one unit to run. Units should always start with an `IO_readCSV`
unit.

### Adding New Units

If creating a test for a new type of unit (for example, if we did not have LASSO, and the current PR was hoping to add
LASSO), the `unit_shortnames` object must first be updated. Inside, the keys represent a shorthand for referring to the
unit. We might named our LASSO unit `REG_lasso`. The value of the key must be the name of the flavor's asset file. If
LASSO existed in a file named `pyml:model:lasso_regression:sklearn.j2.py`, the key for LASSO would be "pyml:model:
lasso_regression:sklearn.j2.py". Note that double quotes are required if the unit name has a colon (because of the YAML
standard).

When adding new units, we recommend creating several tests to check different usage scenarios. For example, if a new
MinMax Scaler was added, at least three unit tests should be created: testing the case of `regrssion`, `classification`,
and `clustering.` See the other tests in the YALM file for known-working configurations.
