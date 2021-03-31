import _ from "underscore";

import {deepClone} from "../utils";

import monitors from "../allowed_monitors";
import allowedResults from "../allowed_results";
import postProcessors from "../allowed_post-processors";

const allowedMonitors = [
    monitors.standard_output,
    monitors.convergence_ionic,
    monitors.convergence_electronic
];

const allowedPostProcessors = [
    postProcessors.error_handler,
    postProcessors.prepare_restart,
    postProcessors.remove_non_zero_weight_kpoints,
];

// helper function to introduce HSE, GW to the tree in a programmatic manner
const getTreeKeyWithMixin = (branch, flavorKey, mixinName) => {
    const addPostfix = (name) => name + "_" + mixinName;
    const flavor = branch[flavorKey];
    const adjustedFlavor = deepClone(flavor);
    delete adjustedFlavor.isDefault;
    // assuming that mixins are only relevant for INCAR
    adjustedFlavor.input.forEach(inputObject => {
        if (inputObject.name === "INCAR") {
            inputObject.templateName = addPostfix(inputObject.templateName || inputObject.name);
        }
    });
    return {[addPostfix(flavorKey).toLowerCase()]: adjustedFlavor};
};

const tree = {
    "vasp": {
        "postProcessors": allowedPostProcessors,
        "monitors": allowedMonitors,
        "results": _.without(allowedResults,
            "phonon_dos",
            "phonon_dispersions",
        ),
        "flavors": {
            "vasp": {
                isDefault: true,
                "input": [
                    {
                        name: 'INCAR',
                    },
                    {
                        name: 'KPOINTS',
                    },
                    {
                        name: 'POSCAR',
                    }
                ],
                "results": [
                    'total_energy',
                    'total_energy_contributions',
                    'pressure',
                    'fermi_energy',
                    'atomic_forces',
                    'total_force',
                    'stress_tensor'
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic
                ],

            },
            "vasp_bands": {
                "input": [
                    {
                        name: 'INCAR',
                        templateName: 'INCAR_BANDS',
                    },
                    {
                        name: 'KPOINTS',
                        templateName: 'KPOINTS_BANDS',
                    },
                    {
                        name: 'POSCAR',
                        templateName: '',
                    }
                ],
                "results": [
                    'band_structure',
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic
                ]

            },
            "vasp_nscf": {
                "input": [
                    {
                        name: 'INCAR',
                        templateName: 'INCAR_BANDS'
                    },
                    {
                        name: 'KPOINTS',
                        templateName: 'KPOINTS'
                    },
                    {
                        name: 'POSCAR',
                        templateName: 'POSCAR'
                    }
                ],
                "results": [
                    'band_gaps',
                    'fermi_energy',
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic
                ]
            },
            "vasp_relax": {
                "input": [
                    {
                        name: 'INCAR',
                        templateName: 'INCAR_RELAX'
                    },
                    {
                        name: 'KPOINTS',
                        templateName: 'KPOINTS'
                    },
                    {
                        name: 'POSCAR',
                        templateName: 'POSCAR'
                    }
                ],
                "results": [
                    'total_energy',
                    'atomic_forces',
                    'fermi_energy',
                    'pressure',
                    'stress_tensor',
                    'total_force',
                    'final_structure'
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic,
                    monitors.convergence_ionic
                ],
                "postProcessors": [
                    postProcessors.prepare_restart,
                ]
            },
            "vasp_vc_relax": {
                "input": [
                    {
                        name: 'INCAR',
                        templateName: 'INCAR_VC_RELAX'
                    },
                    {
                        name: 'KPOINTS',
                        templateName: 'KPOINTS'
                    },
                    {
                        name: 'POSCAR',
                        templateName: 'POSCAR'
                    }
                ],
                "results": [
                    'total_energy',
                    'atomic_forces',
                    'fermi_energy',
                    'pressure',
                    'stress_tensor',
                    'total_force',
                    'final_structure',
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic,
                    monitors.convergence_ionic
                ],
                "postProcessors": [
                    postProcessors.prepare_restart,
                ]

            },
            "vasp_zpe": {
                "input": [
                    {
                        name: 'INCAR',
                        templateName: 'INCAR_ZPE'
                    },
                    {
                        name: 'KPOINTS',
                        templateName: 'KPOINTS'
                    },
                    {
                        name: 'POSCAR',
                        templateName: 'POSCAR'
                    }
                ],
                "results": [
                    'total_energy',
                    'fermi_energy',
                    'pressure',
                    'atomic_forces',
                    'stress_tensor',
                    'total_force',
                    'zero_point_energy'
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic,
                    monitors.convergence_ionic
                ],
            },
            "vasp_kpt_conv": {
                // kpoint convergence => not including kgrid mixin
                "input": [
                    {
                        name: 'INCAR',
                        templateName: 'INCAR'
                    },
                    {
                        name: 'KPOINTS',
                        templateName: 'KPOINTS_CONV'
                    },
                    {
                        name: 'POSCAR',
                        templateName: 'POSCAR'
                    }
                ],
                "results": [
                    'total_energy',
                    'total_energy_contributions',
                    'pressure',
                    'fermi_energy',
                    'atomic_forces',
                    'total_force',
                    'stress_tensor'
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic
                ],
            },
            "vasp_vc_relax_conv": {
                "input": [
                    {
                        name: 'INCAR',
                        templateName: 'INCAR_VC_RELAX'
                    },
                    {
                        name: 'KPOINTS',
                        templateName: 'KPOINTS_CONV'
                    },
                    {
                        name: 'POSCAR',
                        templateName: 'POSCAR'
                    }
                ],
                "results": [
                    'total_energy',
                    'total_energy_contributions',
                    'pressure',
                    'fermi_energy',
                    'atomic_forces',
                    'total_force',
                    'stress_tensor'
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic,
                    monitors.convergence_ionic
                ],
            },
            "vasp_neb": {
                "isMultiMaterial": true,
                "input": [
                    {
                        name: 'INCAR',
                        templateName: 'INCAR_NEB'
                    },
                    {
                        name: 'KPOINTS',
                        templateName: 'KPOINTS'
                    }
                ],
                "results": [
                    "reaction_energy_barrier",
                    "reaction_energy_profile",
                ],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "vasp_neb_initial": {
                "isMultiMaterial": true,
                "input": [
                    {
                        name: 'INCAR',
                        templateName: 'INCAR_NEB_INITIAL_FINAL',
                    },
                    {
                        name: 'KPOINTS',
                    },
                    {
                        name: 'POSCAR',
                        templateName: 'POSCAR_NEB_INITIAL'
                    }
                ],
                "results": [
                    'total_energy',
                    'total_energy_contributions',
                    'pressure',
                    'fermi_energy',
                    'atomic_forces',
                    'total_force',
                    'stress_tensor'
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic
                ],

            },
            "vasp_neb_final": {
                "isMultiMaterial": true,
                "input": [
                    {
                        name: 'INCAR',
                        templateName: 'INCAR_NEB_INITIAL_FINAL',
                    },
                    {
                        name: 'KPOINTS',
                    },
                    {
                        name: 'POSCAR',
                        templateName: 'POSCAR_NEB_FINAL'
                    }
                ],
                "results": [
                    'total_energy',
                    'total_energy_contributions',
                    'pressure',
                    'fermi_energy',
                    'atomic_forces',
                    'total_force',
                    'stress_tensor'
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic
                ],

            },
        }
    }
};

const flavorsBranch = tree["vasp"]["flavors"];
const mixedFlavorsBranch = {};

// ADD HSE
["vasp", "vasp_bands", "vasp_nscf"].forEach(key => {
    Object.assign(mixedFlavorsBranch, getTreeKeyWithMixin(flavorsBranch, key, "HSE"))
});

// update vasp flavors in tree
tree["vasp"]["flavors"] = Object.assign({}, flavorsBranch, mixedFlavorsBranch);

export default tree;
