import ESPRESSO_DATA from "./espresso/data";
import JUPYTERLAB_DATA from "./jupyterLab/data";
import ML_DATA from "./ml/data";
import NWCHEM_DATA from "./nwchem/data";
import PYTHON_DATA from "./python/data";
import SHELL_DATA from "./shell/data";
import VASP_DATA from "./vasp/data";

const APP_DATA = {
    espresso: ESPRESSO_DATA,
    jupyterLab: JUPYTERLAB_DATA,
    ml: ML_DATA,
    nwchem: NWCHEM_DATA,
    python: PYTHON_DATA,
    shell: SHELL_DATA,
    vasp: VASP_DATA,
};

/**
 * Given an application name, return the applications's data.
 * @param appName {str}
 * @returns {object}
 */
export function getAppData(appName) {
    if (!(appName in APP_DATA)) {
        throw new Error(`${appName} is not a known application with data.`);
    }
    return APP_DATA[appName];
}
