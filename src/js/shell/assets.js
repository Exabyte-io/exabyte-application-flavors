import {makeObjectsFromContextProviderNames, readAssetFile} from "../utils";

const applicationName = "shell";
const executableName = "sh";

// Here, we're returning a delayed-evaluation lambda, to avoid loading the asset files in scenarios where they're not
// available, like on the client.
export default () => {
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

    return allAssets.map(a => makeObjectsFromContextProviderNames(a));
};
