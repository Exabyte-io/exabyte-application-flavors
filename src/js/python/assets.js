import {makeObjectsFromContextProviderNames, readAssetFile} from "../utils";

const applicationName = "python";
const executableName = "python";

// Here, we're returning a delayed-evaluation lambda, to avoid loading the asset files in scenarios where they're not
// available, like on the client.
export default () => {
    const allAssets = [
        /*
         *  PYTHON
         */
        {
            "content": readAssetFile(applicationName, "hello_world.pyi"),
            "name": "hello_world.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile(applicationName, "requirements.j2.txt"),
            "name": "requirements.txt",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile(applicationName, "espresso_xml_get_qpt_irr.pyi"),
            "name": "espresso_xml_get_qpt_irr.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "requirements.j2.txt"),
            "name": "pyml_requirements.txt",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName,
        },
        {
            "content": readAssetFile("python/ml", "pyml:setup_variables_packages.pyi"),
            "name": "pyml_settings.py",
            "contextProviders": [
                "MLSettingsDataManager",
            ],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:custom.pyi"),
            "name": "pyml_custom.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName,
        },
        {
            "content": readAssetFile("python/ml", "pyml:data_input:read_csv:pandas.pyi"),
            "name": "data_input_read_csv_pandas.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:data_input:train_test_split:sklearn.pyi"),
            "name": "data_input_train_test_split_sklearn.py",
            "contextProviders": [
                "MLTrainTestSplitDataManager"
            ],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:pre_processing:min_max_scaler:sklearn.pyi"),
            "name": "pre_processing_min_max_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:pre_processing:remove_duplicates:pandas.pyi"),
            "name": "pre_processing_remove_duplicates_pandas.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:pre_processing:remove_missing:pandas.pyi"),
            "name": "pre_processing_remove_missing_pandas.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:pre_processing:standardization:sklearn.pyi"),
            "name": "pre_processing_standardization_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:model:adaboosted_trees_regression:sklearn.pyi"),
            "name": "model_adaboosted_trees_regression_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:model:bagged_trees_regression:sklearn.pyi"),
            "name": "model_bagged_trees_regression_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:model:gradboosted_trees_regression:sklearn.pyi"),
            "name": "model_gradboosted_trees_regression_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:model:k_means_clustering:sklearn.pyi"),
            "name": "model_k_means_clustering_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:model:kernel_ridge_regression:sklearn.pyi"),
            "name": "model_kernel_ridge_regression_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:model:lasso_regression:sklearn.pyi"),
            "name": "model_lasso_regression_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:model:multilayer_perceptron:sklearn.pyi"),
            "name": "model_mlp_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:model:random_forest_classification:sklearn.pyi"),
            "name": "model_random_forest_classification_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:model:gradboosted_classification:sklearn.pyi"),
            "name": "model_gradboosted_classification_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:model:random_forest_regression:sklearn.pyi"),
            "name": "model_random_forest_regression_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:model:ridge_regression:sklearn.pyi"),
            "name": "model_ridge_regression_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:post_processing:parity_plot:matplotlib.pyi"),
            "name": "post_processing_parity_plot_matplotlib.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:post_processing:pca_2d_clusters:matplotlib.pyi"),
            "name": "post_processing_pca_2d_clusters_matplotlib.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },
        {
            "content": readAssetFile("python/ml", "pyml:post_processing:roc_curve:sklearn.pyi"),
            "name": "post_processing_roc_curve_sklearn.py",
            "contextProviders": [],
            "applicationName": applicationName,
            "executableName": executableName
        },


    ];

    return allAssets.map(a => makeObjectsFromContextProviderNames(a));
};
