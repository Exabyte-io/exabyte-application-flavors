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
            "pyml:data_input:read_csv:pandas": {
                "input": [
                    {
                        "name": "data_input_read_csv_pandas.py",
                        "templateName": "data_input_read_csv_pandas.py"
                    },
                ],
                "monitors": [
                    monitors.standard_output
                ]
            },
            "pyml:model:multilayer_perceptron:sklearn": {
                "input": [
                    {
                        "name": "model_multilayer_perceptron_sklearn.py",
                        "templateName": "model_mlp_sklearn.py"
                    },
                ],
                "monitors": [
                    monitors.standard_output
                ]
            },
            "pyml:pre_processing:standardization:sklearn": {
                "input": [
                    {
                        "name": "pre_processing_standardization_sklearn.py",
                        "templateName": "pre_processing_standardization_sklearn.py"
                    },
                ],
                "monitors": [
                    monitors.standard_output
                ]
            },
            "pyml:post_processing_parity_plot_matplotlib": { // Name of the flavor
                "input": [
                    {
                        "name": "post_processing_parity_plot_matplotlib.py", // Name that appears on web-app
                        "templateName": "post_processing_parity_plot_matplotlib.py" // Name as in assets.js
                    },
                ],
                "monitors": [
                    monitors.standard_output
                ]
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
                ]
            },
            "pyml:custom": {
                "input": [
                    {
                        "name": "pyml_custom.py",
                        "templateName": "pyml_custom.py"
                    }
                ]
            }
        }
    }
}
