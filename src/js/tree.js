import ESPRESSO_TREE from "./espresso/tree";
import JUPYTERLAB_TREE from "./jupyterLab/tree";
import ML_TREE from "./ml/tree";
import NWCHEM_TREE from "./nwchem/tree";
import PYTHON_TREE from "./python/tree";
import SHELL_TREE from "./shell/tree";
import VASP_TREE from "./vasp/tree";

const APP_TREES = {
    espresso: ESPRESSO_TREE,
    jupyterLab: JUPYTERLAB_TREE,
    exabyteml: ML_TREE,
    nwchem: NWCHEM_TREE,
    python: PYTHON_TREE,
    shell: SHELL_TREE,
    vasp: VASP_TREE,
};

const _expanded = {};

/**
 * @summary Given an application name, return the applications's tree.
 *          Expands and caches the tree to contain parent level attributes for flavors.
 * @param appName {string}
 * @returns {object}
 */
export function getAppTree(appName) {
    if (!(appName in APP_TREES)) {
        throw new Error(`${appName} is not a known application with a tree.`);
    }
    if (Object.keys(_expanded).includes(appName)) {
        return _expanded[appName];
    }
    const executables = APP_TREES[appName];
    Object.keys(executables).forEach((execName) => {
        const exec = executables[execName];
        Object.keys(exec.flavors).forEach((flavorName) => {
            const flavor = exec.flavors[flavorName];
            flavor.applicationName = appName;
            flavor.executableName = execName;
        });
    });
    _expanded[appName] = executables;
    return executables;
}
