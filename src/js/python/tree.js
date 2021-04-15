import monitors from "../allowed_monitors";

export default {
    "python": {
        "monitors": [
            monitors.standard_output
        ],
        "results": [],
        "flavors": {
            "hello_world": {
                "input": [
                    {
                        "name": "script.py",
                        "templateName": "hello_world.py",
                    },
                    {
                        "name": "requirements.txt",
                    }
                ],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "espresso_xml_get_qpt_irr": {
                "input": [
                    {
                        "name": "espresso_xml_get_qpt_irr.py",
                    },
                ],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "pyml:setup_variables_packages": {
                "input": [
                    {
                        "name": "settings.py",
                        "templateName": "pyml_settings.py"
                    },
                    {
                        "name": "requirements.txt",
                        "templateName": "pyml_requirements.txt"
                    }
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:custom": {
                "input": [
                    {
                        "name": "pyml_custom.py",
                        "templateName": "pyml_custom.py"
                    }
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:data_input:read_csv:pandas": {
                "input": [
                    {
                        "name": "data_input_read_csv_pandas.py",
                        "templateName": "data_input_read_csv_pandas.py"
                    }
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:data_input:train_test_split:sklearn": {
                "input": [
                    {
                        "name": "data_input_train_test_split_sklearn.py",
                        "templateName": "data_input_train_test_split_sklearn.py"
                    }
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:pre_processing:min_max_scaler:sklearn": {
                "input": [
                    {
                        "name": "pre_processing_min_max_sklearn.py",
                        "templateName": "pre_processing_min_max_sklearn.py"
                    }
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:pre_processing:remove_duplicates:pandas": {
                "input": [
                    {
                        "name": "pre_processing_remove_duplicates_pandas.py",
                        "templateName": "pre_processing_remove_duplicates_pandas.py"
                    }
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:pre_processing:remove_missing:pandas": {
                "input": [
                    {
                        "name": "pre_processing_remove_missing_pandas.py",
                        "templateName": "pre_processing_remove_missing_pandas.py"
                    }
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:pre_processing:standardization:sklearn": {
                "input": [
                    {
                        "name": "pre_processing_standardization_sklearn.py",
                        "templateName": "pre_processing_standardization_sklearn.py"
                    }
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:model:adaboosted_trees_regression:sklearn": {
                "input": [
                    {
                        "name": "model_adaboosted_trees_regression_sklearn.py",
                        "templateName": "model_adaboosted_trees_regression_sklearn.py"
                    }
                ],
                "monitors": [monitors.standard_output],
                "results": [
                    "workflow:pyml_predict"
                ],
            },
            "pyml:model:bagged_trees_regression:sklearn": {
                "input": [
                    {
                        "name": "model_bagged_trees_regression_sklearn.py",
                        "templateName": "model_bagged_trees_regression_sklearn.py"
                    }
                ],
                "results": [
                    "workflow:pyml_predict"
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:model:gradboosted_trees_regression:sklearn": {
                "input": [
                    {
                        "name": "model_gradboosted_trees_regression_sklearn.py",
                        "templateName": "model_gradboosted_trees_regression_sklearn.py"
                    }
                ],
                "results": [
                    "workflow:pyml_predict"
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:model:k_means_clustering:sklearn": {
                "input": [
                    {
                        "name": "model_k_means_clustering_sklearn.py",
                        "templateName": "model_k_means_clustering_sklearn.py"
                    }
                ],
                "results": [
                    "workflow:pyml_predict"
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:model:kernel_ridge_regression:sklearn": {
                "input": [
                    {
                        "name": "model_kernel_ridge_regression_sklearn.py",
                        "templateName": "model_kernel_ridge_regression_sklearn.py"
                    }
                ],
                "results": [
                    "workflow:pyml_predict"
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:model:lasso_regression:sklearn": {
                "input": [
                    {
                        "name": "model_lasso_regression_sklearn.py",
                        "templateName": "model_lasso_regression_sklearn.py"
                    }
                ],
                "results": [
                    "workflow:pyml_predict"
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:model:multilayer_perceptron:sklearn": {
                "input": [
                    {
                        "name": "model_mlp_sklearn.py",
                        "templateName": "model_mlp_sklearn.py"
                    }
                ],
                "results": [
                    "workflow:pyml_predict"
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:model:random_forest_classification:sklearn": {
                "input": [
                    {
                        "name": "model_random_forest_classification_sklearn.py",
                        "templateName": "model_random_forest_classification_sklearn.py"
                    }
                ],
                "results": [
                    "workflow:pyml_predict"
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:model:random_forest_regression:sklearn": {
                "input": [
                    {
                        "name": "model_random_forest_regression_sklearn.py",
                        "templateName": "model_random_forest_regression_sklearn.py"
                    }
                ],
                "results": [
                    "workflow:pyml_predict"
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:model:ridge_regression:sklearn": {
                "input": [
                    {
                        "name": "model_ridge_regression_sklearn.py",
                        "templateName": "model_ridge_regression_sklearn.py"
                    }
                ],
                "results": [
                    "workflow:pyml_predict"
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:post_processing:parity_plot:matplotlib": {
                "input": [
                    {
                        "name": "post_processing_parity_plot_matplotlib.py",
                        "templateName": "post_processing_parity_plot_matplotlib.py"
                    }
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:post_processing:pca_2d_clusters:matplotlib": {
                "input": [
                    {
                        "name": "post_processing_pca_2d_clusters_matplotlib.py",
                        "templateName": "post_processing_pca_2d_clusters_matplotlib.py"
                    }
                ],
                "monitors": [monitors.standard_output],
            },
            "pyml:post_processing:roc_curve:sklearn": {
                "input": [
                    {
                        "name": "post_processing_roc_curve_sklearn.py",
                        "templateName": "post_processing_roc_curve_sklearn.py"
                    }
                ],
                "monitors": [monitors.standard_output],
            },
        }
    }
}
