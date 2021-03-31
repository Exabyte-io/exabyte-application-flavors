import {makeObjectsFromContextProviderNames, readAssetFile} from "../utils";

const applicationName = "jupyterLab"
const executableName = "jupyter"

const allAssets = [
    {
        "content": readAssetFile(applicationName, "install.j2.sh"),
        "name": "install.sh",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "configure.j2.py"),
        "name": "config.py",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "configure.j2.sh"),
        "name": "configure.sh",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },

];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
