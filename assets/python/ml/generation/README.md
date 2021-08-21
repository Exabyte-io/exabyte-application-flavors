# PythonML

This directory contains the work corresponding to the PythonML implementation. Further documentation can be found here:

https://docs.exabyte.io/software-directory/machine-learning/python-ml/overview/

## Current Status

This directory is in the midst of an overhaul. Previously, we'd been generating flavors by hand, which resulted in a
large number of files that are largely similar. As a result, we have been slowly replacing this directory with a
templating approach. 

Currently, any flavors prefixed with `pyml:model` are automatically templated. Future plans include the automated
generation of the following flavor prefixes:
- `pyml:data_input`
- `pyml:post_processing`
- `pyml:pre_processing`

In addition, we plan to add machinery that will automatically update the package's `assets.js` and `tree.js` with
the appropriate flavors from this directory, at render-time.

# Templating

Our templating machinery works as follows:

1. The file `render_templates.py` is executed. This file is the main driver of any templating that we conduct.
2. The `config.yaml` file is read in, which contains general configuration for the rendering. Currently, it is only used
    to keep track of the boilerplate in comment box at the top of each flavor.
3. The `model.yaml` file (more on that later) is read, which contains general settings for each individual model type,
    along with anything else the `render_templates.py` script needs to know in order to render the file. For example,
    it includes information about whether the model is a regressor or classifier, any default arguments, etc.
4. The appropriate template is found, and the model's configuration is used to render out a `.pyi` file. This file is
    what the user receives in the web-app when they add a flavor to their machine learning workflow.


## Files

Several files are used to support our rendering. They're enumerated below.

### render_templates.py
This file is the main driver of the templating approach, reading in the various other files needed, and doing any
calculations necessary for the rendering to occur.

### config.yaml
This file contains project-level settings, that affect all models.

The possible settings are enumerated below.

#### Project-Level Settings
- `pyml_render_output_directory` - Path where the asset files will be output into when rendered.
- `documentation_box_common_text` - contains boilerplate that goes into the documentation box for different models.
    Current options include:
  - `regression` - The boilerplate documentation text used for all regression models.
  - `classification` - The boilerplate documentation text used for all classification models.
  - `clustering` - The boilerplate documentation text used for all clustering models.

### model.yaml

This file contains settings specific to individual models, and is used to render out the `pyml:model` flavors. 

Each model is stored as a separate YAML document within this file (separated by three dashes, `---`).

Several common settings are found in the case of all models, enumerated below:

#### Model-Specific Settings

- `name` - A string containing the name of the model
- `category` - Problem category the model addresses. Can be `regression`, `classification`, or `clustering`
- `provider` - Name of the Python package that provides this functionality (such as pandas or sklearn)
- `ensemble` - Whether the model contains other models or not. If the model is an ensemble, additional settings for the
                base estimator must be specified (more on that later).
- `description` - A string containing a short description of what the model does. This is rendered into the comment box.
- `imports` - A list of packages that are needed for the model template to function (e.g. `sklearn.linear_model`).
- `model_class` - Import path from the base package providing a model, to the actual class implementing the model. For
                    example, Scikit-Learn implements its LASSO model in `sklearn.linear_model.Lasso`.
- `model_default_args` - A list of `key`:`value` pairs that will be passed into the model's `__init__` by default when
                        the model flavor is rendered. For example, if we want to specify a default L1-regularization
                        term as 0.1 when a user loads an sklearn LASSO model, we would provide `alpha:0.1` as one of
                        the keys.

In the case of ensemble models (or any other approach which takes in a model), a base estimator may need to be
specified. For example, sklearn implements a BaggingRegressor that can take in other estimators as its base estimator.
We have set a Decision Tree Regressor as its base estimator, but the user can change this if needed. In the case of
ensemble models that require the definition of a base estimator, the following additional options can be specified:

- `base_estimator_class` - Similar to `model_class` above, this is an import path from the base package providing
                            the estimator to its implementation. For example, Sklearn implements its Decision Tree
                            Regressor in `sklearn.tree.DecisionTreeRegressor`.
- `base_estimator_default_args` - Similar to `model_default_args` above. This is a list of default parameters that will
                                    be passed to the model's `__init__` in the rendered script. They are specified as a
                                    set of `key`:`value` pairs. For example, if we wanted our decision tree to use the
                                    Mean Squared Error as its splitting criterion by default, we would specify
                                    `criterion`:`"mse"` as one of the key:value pairs being passed in.
