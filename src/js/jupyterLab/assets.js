import {makeObjectsFromContextProviderNames} from "../utils";

import INSTALL_SH from "./assets/install.sh";
import CONFIG_PY from "./assets/configure.py";
import CONFIGURE_SH from "./assets/configure.sh";

const allAssets = [
    {
        "content": INSTALL_SH,
        "name": "install.sh",
        "contextProviders": [],
        "applicationName": "jupyterLab",
        "executableName": "jupyter"
    },
    {
        "content": CONFIG_PY,
        "name": "config.py",
        "contextProviders": [],
        "applicationName": "jupyterLab",
        "executableName": "jupyter"
    },
    {
        "content": CONFIGURE_SH,
        "name": "configure.sh",
        "contextProviders": [],
        "applicationName": "jupyterLab",
        "executableName": "jupyter"
    },

];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
