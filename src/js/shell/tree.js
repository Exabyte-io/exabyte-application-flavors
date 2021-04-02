import monitors from "../allowed_monitors";
import allowedResults from "../allowed_results";

export default {
    "sh": {
        "monitors": [
            monitors.standard_output
        ],
        "results": allowedResults,
        "flavors": {
            "hello_world": {
                "input": [
                    {
                        "name": "hello_world.sh",
                    }
                ],
                "monitors": [
                    monitors.standard_output
                ]
            },
            "job_espresso_pw_scf": {
                "input": [
                    {
                        "name": "job_espresso_pw_scf.sh",
                    }
                ],
                "monitors": [
                    monitors.standard_output
                ]
            },
            "espresso_link_outdir_save": {
                "input": [
                    {
                        "name": "espresso_link_outdir_save.sh",
                    }
                ],
                "monitors": [
                    monitors.standard_output
                ]
            },
            "espresso_collect_dynmat": {
                "input": [
                    {
                        "name": "espresso_collect_dynmat.sh",
                    }
                ],
                "monitors": [
                    monitors.standard_output
                ]
            },
            "bash_vasp_prepare_neb_images": {
                "isMultiMaterial": true,
                "input": [
                    {
                        "name": "bash_vasp_prepare_neb_images.sh",
                    }
                ],
                "monitors": [
                    monitors.standard_output
                ]
            }
        }
    }
}
