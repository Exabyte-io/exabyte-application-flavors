import {makeObjectsFromContextProviderNames, readAssetFile} from "../utils";

const applicationName = "python";
const executableName = "python";

const allAssets = [
    /*
     *  PYTHON
     */
    {
        "content": readAssetFile(applicationName, "hello_world.py.jinja2"),
        "name": "hello_world.py",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "requirements.txt.jinja2"),
        "name": "requirements.txt",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "espresso_xml_get_qpt_irr.py.jinja2"),
        "name": "espresso_xml_get_qpt_irr.py",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile("python/ml", "pyml:data_input:read_csv:pandas.py.jinja2"),
        "name": "data_input_read_csv_pandas.py",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile("python/ml", "pyml:pre_processing:standardization:sklearn.py.jinja2"),
        "name": "pre_processing_standardization_sklearn.py",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile("python/ml", "pyml:model:multilayer_perceptron:sklearn.py.jinja2"),
        "name": "model_mlp_sklearn.py",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile("python/ml", "pyml:setup_variables_packages.py.jinja2"),
        "name": "pyml_settings.py",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile("python/ml", "pyml:post_processing:parity_plot:matplotlib.py.jinja2"),
        "name": "post_processing_parity_plot_matplotlib.py",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile("python/ml", "requirements.txt.jinja2"),
        "name": "pyml_requirements.txt",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName,
    },
    {
        "content": readAssetFile("python/ml", "pyml:custom.py.jinja2"),
        "name": "pyml_custom.py",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName,
    }

];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
