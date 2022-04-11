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

/**
 * Given an application name, return the applications's tree.
 * @param appName {str}
 * @returns {object}
 */
export function getAppTree(appName) {
    if (!(appName in APP_TREES)) {
        throw new Error(`${appName} is not a known application with a tree.`);
    }
    return APP_TREES[appName];
}
