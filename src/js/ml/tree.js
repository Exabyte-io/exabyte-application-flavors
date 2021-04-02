import monitors from "../allowed_monitors";

export default {
    "train": {
        "isDefault": true,
        "monitors": [
            monitors.standard_output
        ],
        "results": [],
        "flavors": {
            "train": {
                "isDefault": true,
                "input": [],
                "monitors": [
                    monitors.standard_output
                ],
            }
        }
    },
    "score": {
        "isDefault": false,
        "monitors": [
            monitors.standard_output
        ],
        "results": [],
        "flavors": {
            "isDefault": true,
            "score": {
                "input": [],
                "monitors": [
                    monitors.standard_output
                ],
            }
        }
    }
}
