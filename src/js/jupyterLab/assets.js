import {makeObjectsFromContextProviderNames, readAssetFile} from "../utils";

const applicationName = "jupyterLab"
const executableName = "jupyter"

const allAssets = [
    {
        "content": readAssetFile(applicationName, "install.sh.jinja2"),
        "name": "install.sh",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "configure.py.jinja2"),
        "name": "config.py",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "configure.sh.jinja2"),
        "name": "configure.sh",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": executableName
    },

];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
