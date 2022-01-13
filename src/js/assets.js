import ESPRESSO_INPUT_TEMPLATES from "./espresso/assets";
import JUPYTER_INPUT_TEMPLATES from "./jupyterLab/assets";
import NWCHEM_INPUT_TEMPLATES from "./nwchem/assets";
import PYTHON_INPUT_TEMPLATES from "./python/assets";
import SHELL_INPUT_TEMPLATES from "./shell/assets";
import VASP_INPUT_TEMPLATES from "./vasp/assets";

export function getAllAppTemplates() {
    return [].concat.apply(
        [],
        [
            ESPRESSO_INPUT_TEMPLATES(),
            SHELL_INPUT_TEMPLATES(),
            PYTHON_INPUT_TEMPLATES(),
            VASP_INPUT_TEMPLATES(),
            JUPYTER_INPUT_TEMPLATES(),
            NWCHEM_INPUT_TEMPLATES(),
        ],
    );
}
