import {makeObjectsFromContextProviderNames} from "../utils";

import PYTHON_HELLO_WORLD from "./assets/hello_world.py";
import PYTHON_REQUIREMENTS_TXT from "./assets/requirements.txt";
import ESPRESSO_XML_GET_QPT_IRR from "./assets/espresso_xml_get_qpt_irr.py";

import PYML_DATAINPUT_READCSV_PANDAS from "./assets/ml/pyml:data_input:read_csv:pandas.py";
import PYML_MODEL_MUTILAYERPERCEPTRON_SKLEARN from "./assets/ml/pyml:model:multilayer_perceptron:sklearn.py";
import PYML_PREPROCESSING_STANDARDIZATION_SKLEARN from "./assets/ml/pyml:pre_processing:standardization:sklearn.py";
import PYML_SETUPVARIABLESPACKAGES from "./assets/ml/pyml:setup_variables_packages.py";
import PYML_POSTPROCESSING_PARITYPLOT_MATPLOTLIB from "./assets/ml/pyml:post_processing:parity_plot:matplotlib.py"
import PYML_REQUIREMENTS_TXT from "./assets/ml/requirements.txt";
import PYML_CUSTOM from "./assets/ml/pyml:custom.py"

const allAssets = [
    /*
     *  PYTHON
     */
    {
        "content": PYTHON_HELLO_WORLD,
        "name": "hello_world.py",
        "contextProviders": [],
        "applicationName": "python",
        "executableName": "python"
    },
    {
        "content": PYTHON_REQUIREMENTS_TXT,
        "name": "requirements.txt",
        "contextProviders": [],
        "applicationName": "python",
        "executableName": "python"
    },
    {
        "content": ESPRESSO_XML_GET_QPT_IRR,
        "name": "espresso_xml_get_qpt_irr.py",
        "contextProviders": [],
        "applicationName": "python",
        "executableName": "python"
    },
    {
        "content": PYML_DATAINPUT_READCSV_PANDAS,
        "name": "data_input_read_csv_pandas.py",
        "contextProviders": [],
        "applicationName": "python",
        "executableName": "python"
    },
    {
        "content": PYML_PREPROCESSING_STANDARDIZATION_SKLEARN,
        "name": "pre_processing_standardization_sklearn.py",
        "contextProviders": [],
        "applicationName": "python",
        "executableName": "python"
    },
    {
        "content": PYML_MODEL_MUTILAYERPERCEPTRON_SKLEARN,
        "name": "model_mlp_sklearn.py",
        "contextProviders": [],
        "applicationName": "python",
        "executableName": "python"
    },
    {
        "content": PYML_SETUPVARIABLESPACKAGES,
        "name": "pyml_settings.py",
        "contextProviders": [],
        "applicationName": "python",
        "executableName": "python"
    },
    {
        "content": PYML_POSTPROCESSING_PARITYPLOT_MATPLOTLIB,
        "name": "post_processing_parity_plot_matplotlib.py",
        "contextProviders": [],
        "applicationName": "python",
        "executableName": "python"
    },
    {
        "content": PYML_REQUIREMENTS_TXT,
        "name": "pyml_requirements.txt",
        "contextProviders": [],
        "applicationName": "python",
        "executableName": "python",
    },
    {
        "content": PYML_CUSTOM,
        "name": "pyml_custom.py",
        "contextProviders": [],
        "applicationName": "python",
        "executableName": "python",
    }

];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
