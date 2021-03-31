import {makeObjectsFromContextProviderNames} from "../utils";

import BASH_HELLO_WORLD from "./assets/bash_hello_world.sh";
import BASH_ESPRESSO_PW_SCF from "./assets/bash_job_espresso_pw_scf.sh";
import BASH_ESPRESSO_COLLECT_DYNMAT from "./assets/bash_espresso_collect_dynmat.sh";
import BASH_VASP_PREPARE_NEB_IMAGES from "./assets/bash_vasp_prepare_neb_images.sh";
import BASH_ESPRESSO_LINK_OUTDIR_SAVE from "./assets/bash_espresso_link_outdir_save.sh";

const allAssets = [
    /*
     *  BASH
     */
    {
        "content": BASH_HELLO_WORLD,
        "name": "hello_world.sh",
        "contextProviders": [],
        "applicationName": "shell",
        "executableName": "sh"
    },
    {
        "content": BASH_ESPRESSO_PW_SCF,
        "name": "job_espresso_pw_scf.sh",
        "contextProviders": [],
        "applicationName": "shell",
        "executableName": "sh"
    },
    {
        "content": BASH_ESPRESSO_LINK_OUTDIR_SAVE,
        "name": "espresso_link_outdir_save.sh",
        "contextProviders": [],
        "applicationName": "shell",
        "executableName": "sh"
    },
    {
        "content": BASH_ESPRESSO_COLLECT_DYNMAT,
        "name": "espresso_collect_dynmat.sh",
        "contextProviders": [],
        "applicationName": "shell",
        "executableName": "sh"
    },
    {
        "content": BASH_VASP_PREPARE_NEB_IMAGES,
        "name": "bash_vasp_prepare_neb_images.sh",
        "contextProviders": ["VASPNEBInputDataManager"],
        "applicationName": "shell",
        "executableName": "sh"
    },
];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
