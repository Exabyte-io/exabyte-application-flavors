import monitors from "../allowed_monitors";

export default {
    "jupyter": {
        "monitors": [
            monitors.standard_output,
            monitors.jupyterNotebookEndpoint,
        ],
        "results": [],
        "flavors": {
            "notebook": {
                "input": [
                    {
                        "name": "install.sh",
                        "templateName": "install.sh",
                    },
                    {
                        "name": "config.py",
                        "templateName": "config.py",
                    },
                    {
                        "name": "configure.sh",
                        "templateName": "configure.sh",
                    }
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.jupyterNotebookEndpoint,
                ],
            }
        }
    }
}
