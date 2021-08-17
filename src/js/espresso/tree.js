import _ from "underscore";

import monitors from "../allowed_monitors";
import allowedResults from "../allowed_results";
import postProcessors from "../allowed_post-processors";

const allowedMonitors = [
    monitors.standard_output,
    monitors.convergence_ionic,
    monitors.convergence_electronic
];

// import postProcessors from "../allowed_post-processors";
const allowedPostProcessors = [
    /* restart logic is handled by restart flag within a (Sub)workflow */
    // postProcessors.prepare_restart,
    postProcessors.remove_non_zero_weight_kpoints,
];

export default {
    "pw.x": {
        "isDefault": true,
        "advancedComputeOptions": true,
        "postProcessors": allowedPostProcessors,
        "monitors": allowedMonitors,
        "results": _.without(allowedResults,
            "phonon_dos",
            "phonon_dispersions",
            "zero_point_energy",
            "band_structure"
        ),
        "flavors": {
            "pw_scf": {
                "isDefault": true,
                "input": [
                    {
                        "name": "pw_scf.in"
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
            "pw_scf_bands_hse": {
                "input": [
                    {
                        "name": "pw_scf_bands_hse.in"
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
            "pw_esm": {
                "input": [
                    {
                        "name": "pw_esm.in"
                    }
                ],
                "results": [
                    'total_energy',
                    'total_energy_contributions',
                    'pressure',
                    'fermi_energy',
                    'atomic_forces',
                    'total_force',
                    'stress_tensor',
                    'potential_profile',
                    'charge_density_profile',
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic
                ],
            },
            "pw_esm_relax": {
                "input": [
                    {
                        "name": "pw_esm_relax.in"
                    }
                ],
                "results": [
                    'total_energy',
                    'total_energy_contributions',
                    'pressure',
                    'fermi_energy',
                    'atomic_forces',
                    'total_force',
                    'stress_tensor',
                    'potential_profile',
                    'charge_density_profile',
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic
                ],
            },
            "pw_nscf": {
                "input": [
                    {
                        "name": "pw_nscf.in"
                    }
                ],
                "results": [
                    'fermi_energy',
                    'band_gaps'
                ],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "pw_bands": {
                "input": [
                    {
                        "name": "pw_bands.in"
                    }
                ],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "pw_relax": {
                "input": [
                    {
                        "name": "pw_relax.in"
                    }
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic,
                    monitors.convergence_ionic
                ],
                "results": [
                    'total_energy',
                    'fermi_energy',
                    'pressure',
                    'atomic_forces',
                    'total_force',
                    'stress_tensor',
                    'final_structure',
                ]
            },
            "pw_vc-relax": {
                "input": [
                    {
                        "name": "pw_vc_relax.in"
                    }
                ],
                "monitors": [
                    monitors.standard_output,
                    monitors.convergence_electronic,
                    monitors.convergence_ionic
                ],
                "results": [
                    'total_energy',
                    'fermi_energy',
                    'pressure',
                    'atomic_forces',
                    'total_force',
                    'stress_tensor',
                    'final_structure',
                ]
            },
            // Temporarily disabled to keep track of. `Subworkflow.addConvergence` is using updateContext instead.
            // TODO: remove or re-enable during next refactoring
            // "pw_scf_kpt_conv": {
            //     "input": [
            //         {
            //             "name": "pw_scf_kpt_conv.in"
            //         }
            //     ],
            //     "results": [
            //         'total_energy',
            //         'fermi_energy',
            //         'pressure',
            //         'atomic_forces',
            //         'total_force',
            //         'stress_tensor'
            //     ],
            //     "monitors": [
            //         monitors.standard_output,
            //         monitors.convergence_electronic
            //     ],
            // },
        }
    },
    "ph.x": {
        "monitors": [
            monitors.standard_output,
        ],
        "results": [
            "phonon_dos",
            "phonon_dispersions",
            "zero_point_energy"
        ],
        "flavors": {
            "ph_path": {
                "input": [
                    {
                        "name": "ph_path.in",
                    }
                ],
                "results": [
                    "phonon_dispersions"
                ],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "ph_grid": {
                "input": [
                    {
                        "name": "ph_grid.in",
                    }
                ],
                "results": [
                    "phonon_dos"
                ],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "ph_gamma": {
                "input": [
                    {
                        "name": "ph_gamma.in",
                    }
                ],
                "results": [
                    "zero_point_energy"
                ],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "ph_init_qpoints": {
                "input": [
                    {
                        "name": "ph_init_qpoints.in",
                    }
                ],
                "results": [],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "ph_grid_restart": {
                "input": [
                    {
                        "name": "ph_grid_restart.in",
                    }
                ],
                "results": [],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "ph_single_irr_qpt": {
                "input": [
                    {
                        "name": "ph_single_irr_qpt.in",
                    }
                ],
                "results": [],
                "monitors": [
                    monitors.standard_output
                ],
            }
        }
    },

    "bands.x": {
        "monitors": [
            monitors.standard_output,
        ],
        "results": ["band_structure"],
        "flavors": {
            "bands": {
                "input": [
                    {
                        "name": "bands.in",
                    }
                ],
                "results": [
                    'band_structure'
                ],
                "monitors": [
                    monitors.standard_output
                ],
            }
        }
    },
    "projwfc.x": {
        "monitors": [
            monitors.standard_output,
        ],
        "results": ["density_of_states"],
        "flavors": {
            "projwfc": {
                "input": [
                    {
                        "name": "projwfc.in",
                    }
                ],
                "results": [
                    'density_of_states'
                ],
                "monitors": [
                    monitors.standard_output
                ],
            }
        }
    },
    "dos.x": {
        "monitors": [
            monitors.standard_output,
        ],
        "results": ["density_of_states"],
        "flavors": {
            "dos": {
                "input": [
                    {
                        "name": "dos.in",
                    }
                ],
                "results": [
                    'density_of_states'
                ],
                "monitors": [
                    monitors.standard_output
                ],
            }
        }
    },
    "pp.x": {
        "monitors": [
            monitors.standard_output,
        ],
        "results": [],
        "flavors": {
            "pp_density": {
                "input": [
                    {
                        "name": "pp_density.in",
                    }
                ],
                "results": [],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "pp_electrostatic_potential": {
                "input": [
                    {
                        "name": "pp_electrostatic_potential.in",
                    }
                ],
                "results": [],
                "monitors": [
                    monitors.standard_output
                ],
            }
        }
    },
    "q2r.x": {
        "monitors": [
            monitors.standard_output,
        ],
        "results": [],
        "flavors": {
            "q2r": {
                "input": [
                    {
                        "name": "q2r.in",
                    }
                ],
                "results": [],
                "monitors": [
                    monitors.standard_output
                ],
            }
        }
    },
    "dynmat.x": {
        "monitors": [
            monitors.standard_output,
        ],
        "results": [],
        "flavors": {
            "dynmat": {
                "input": [
                    {
                        "name": "matdyn_grid.in",
                    }
                ],
                "results": [],
                "monitors": [
                    monitors.standard_output
                ],
            }
        }
    },
    "matdyn.x": {
        "monitors": [
            monitors.standard_output,
        ],
        "results": [
            "phonon_dos",
            "phonon_dispersions"
        ],
        "flavors": {
            "matdyn_grid": {
                "input": [
                    {
                        "name": "matdyn_grid.in",
                    }
                ],
                "monitors": [
                    monitors.standard_output
                ],
                "results": [
                    'phonon_dos'
                ],
            },
            "matdyn_path": {
                "input": [
                    {
                        "name": "matdyn_path.in",
                    }
                ],
                "monitors": [
                    monitors.standard_output
                ],
                "results": [
                    'phonon_dispersions'
                ],
            }
        }
    },
    "neb.x": {
        "monitors": [
            monitors.standard_output,
        ],
        "results": [
            "reaction_energy_barrier",
            "reaction_energy_profile",
        ],
        "flavors": {
            "neb": {
                "isMultiMaterial": true,
                "input": [
                    {
                        "name": "neb.in",
                    }
                ],
                "results": [
                    "reaction_energy_barrier",
                    "reaction_energy_profile",
                ],
                "monitors": [
                    monitors.standard_output
                ],
            }
        }
    },
    "gw.x": {
        "monitors": [
            monitors.standard_output,
        ],
        "results": [
            "band_structure",
            'fermi_energy',
            'band_gaps'
        ],
        "flavors": {
            "gw_bands_plasmon_pole": {
                "input": [
                    {
                        "name": "gw_bands_plasmon_pole.in",
                    }
                ],
                "results": [
                    "band_structure",
                    'fermi_energy',
                    'band_gaps'
                ],
                "monitors": [
                    monitors.standard_output
                ],
            },
            "gw_bands_full_frequency": {
                "input": [
                    {
                        "name": "gw_bands_full_frequency.in",
                    }
                ],
                "results": [
                    "band_structure",
                    'fermi_energy',
                    'band_gaps'
                ],
                "monitors": [
                    monitors.standard_output
                ],
            }
        },
    },
    "average.x": {
        "monitors": [
            monitors.standard_output,
        ],
        "results": [],
        "flavors": {
            "average": {
                "input": [
                    {
                        "name": "average.in",
                    }
                ],
                "results": [],
                "monitors": [
                    monitors.standard_output
                ],
            }
        }
    },
}
