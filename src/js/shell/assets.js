import {makeObjectsFromContextProviderNames, readAssetFile} from "../utils";

const applicationName = "shell";
const executableName = "sh";

const allAssets = [
    /*
     *  BASH
     */
    {
        "content": readAssetFile(applicationName, "bash_hello_world.j2.sh"),
        "name": "hello_world.sh",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "bash_job_espresso_pw_scf.j2.sh"),
        "name": "job_espresso_pw_scf.sh",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "bash_espresso_link_outdir_save.j2.sh"),
        "name": "espresso_link_outdir_save.sh",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "bash_espresso_collect_dynmat.j2.sh"),
        "name": "espresso_collect_dynmat.sh",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "bash_vasp_prepare_neb_images.j2.sh"),
        "name": "bash_vasp_prepare_neb_images.sh",
        "contextProviders": ["VASPNEBInputDataManager"],
        "applicationName": applicationName,
        "executableName": executableName
    },
];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
