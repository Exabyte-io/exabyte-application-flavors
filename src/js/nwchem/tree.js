import _ from "underscore";

import monitors from "../allowed_monitors";
import postProcessors from "../allowed_post-processors";
import results from "../allowed_results";

const allowedMonitors = [monitors.standard_output];
const allowedPostProcessors = [postProcessors.error_handler];
const allowedResults = results;

export default {
    nwchem: {
        isDefault: true,
        advancedComputeOptions: false,
        postProcessors: allowedPostProcessors,
        monitors: allowedMonitors,
        results: _.without(
            allowedResults,
            "atomic_forces",
            "band_gaps",
            "band_structure",
            "density_of_states",
            "fermi_energy",
            "phonon_dispersions",
            "phonon_dos",
            "pressure",
            "stress_tensor",
            "total_force",
            "zero_point_energy",
            "final_structure",
            "magnetic_moments",
            "reaction_energy_barrier",
            "reaction_energy_profile",
            "potential_profile",
            "charge_density_profile",
        ),
        flavors: {
            nwchem_total_energy: {
                isDefault: true,
                input: [
                    {
                        name: "nwchem_total_energy.inp",
                    },
                ],
                results: ["total_energy", "total_energy_contributions"],
                monitors: allowedMonitors,
            },
        },
    },
};
