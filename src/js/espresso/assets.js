import { makeObjectsFromContextProviderNames, readAssetFile } from "../utils";

const applicationName = "espresso";

// Here, we're returning a delayed-evaluation lambda, to avoid loading the asset files in scenarios where they're not
// available, like on the client.
export default () => {
    const allAssets = [
        /*
         *  PW.X
         */
        {
            content: readAssetFile(applicationName, "pw_scf.j2.in"),
            name: "pw_scf.in",
            contextProviders: [
                "KGridFormDataManager",
                "QEPWXInputDataManager",
                "PlanewaveCutoffDataManager",
            ],
            applicationName,
            executableName: "pw.x",
        },
        {
            content: readAssetFile(applicationName, "pw_scf_bands_hse.j2.in"),
            name: "pw_scf_bands_hse.in",
            contextProviders: [
                "QEPWXInputDataManager",
                "PlanewaveCutoffDataManager",
                "QGridFormDataManager",
                "ExplicitKPathFormDataManager",
            ],
            applicationName,
            executableName: "pw.x",
        },
        {
            content: readAssetFile(applicationName, "pw_esm.j2.in"),
            name: "pw_esm.in",
            contextProviders: [
                "KGridFormDataManager",
                "QEPWXInputDataManager",
                "PlanewaveCutoffDataManager",
                "BoundaryConditionsFormDataManager",
            ],
            applicationName,
            executableName: "pw.x",
        },
        {
            content: readAssetFile(applicationName, "pw_esm_relax.j2.in"),
            name: "pw_esm_relax.in",
            contextProviders: [
                "KGridFormDataManager",
                "QEPWXInputDataManager",
                "PlanewaveCutoffDataManager",
                "BoundaryConditionsFormDataManager",
            ],
            applicationName,
            executableName: "pw.x",
        },

        {
            content: readAssetFile(applicationName, "pw_scf_kpt_conv.j2.in"),
            name: "pw_scf_kpt_conv.in",
            contextProviders: ["QEPWXInputDataManager", "PlanewaveCutoffDataManager"],
            applicationName,
            executableName: "pw.x",
        },
        {
            content: readAssetFile(applicationName, "pw_nscf.j2.in"),
            name: "pw_nscf.in",
            contextProviders: [
                "KGridFormDataManager",
                "QEPWXInputDataManager",
                "PlanewaveCutoffDataManager",
            ],
            applicationName,
            executableName: "pw.x",
        },
        {
            content: readAssetFile(applicationName, "pw_relax.j2.in"),
            name: "pw_relax.in",
            contextProviders: [
                "KGridFormDataManager",
                "QEPWXInputDataManager",
                "PlanewaveCutoffDataManager",
            ],
            applicationName,
            executableName: "pw.x",
        },
        {
            content: readAssetFile(applicationName, "pw_vc_relax.j2.in"),
            name: "pw_vc_relax.in",
            contextProviders: [
                "KGridFormDataManager",
                "QEPWXInputDataManager",
                "PlanewaveCutoffDataManager",
            ],
            applicationName,
            executableName: "pw.x",
        },
        {
            content: readAssetFile(applicationName, "pw_bands.j2.in"),
            name: "pw_bands.in",
            contextProviders: [
                "KPathFormDataManager",
                "QEPWXInputDataManager",
                "PlanewaveCutoffDataManager",
            ],
            applicationName,
            executableName: "pw.x",
        },

        /*
         *  PH.X
         */
        {
            content: readAssetFile(applicationName, "ph_grid.j2.in"),
            name: "ph_grid.in",
            contextProviders: ["QGridFormDataManager"],
            applicationName,
            executableName: "ph.x",
        },
        {
            content: readAssetFile(applicationName, "ph_path.j2.in"),
            name: "ph_path.in",
            contextProviders: ["QPathFormDataManager"],
            applicationName,
            executableName: "ph.x",
        },
        {
            content: readAssetFile(applicationName, "ph_gamma.j2.in"),
            name: "ph_gamma.in",
            contextProviders: [],
            applicationName,
            executableName: "ph.x",
        },
        {
            content: readAssetFile(applicationName, "ph_init_qpoints.j2.in"),
            name: "ph_init_qpoints.in",
            contextProviders: ["QGridFormDataManager"],
            applicationName,
            executableName: "ph.x",
        },
        {
            content: readAssetFile(applicationName, "ph_grid_restart.j2.in"),
            name: "ph_grid_restart.in",
            contextProviders: ["QGridFormDataManager"],
            applicationName,
            executableName: "ph.x",
        },
        {
            content: readAssetFile(applicationName, "ph_single_irr_qpt.j2.in"),
            name: "ph_single_irr_qpt.in",
            contextProviders: ["QGridFormDataManager"],
            applicationName,
            executableName: "ph.x",
        },

        /*
         *  MATDYN.X
         */
        {
            content: readAssetFile(applicationName, "matdyn_grid.j2.in"),
            name: "matdyn_grid.in",
            contextProviders: ["IGridFormDataManager"],
            applicationName,
            executableName: "matdyn.x",
        },
        {
            content: readAssetFile(applicationName, "matdyn_path.j2.in"),
            name: "matdyn_path.in",
            contextProviders: ["IPathFormDataManager"],
            applicationName,
            executableName: "matdyn.x",
        },

        /*
         *  BANDS.X
         */
        {
            content: readAssetFile(applicationName, "bands.j2.in"),
            name: "bands.in",
            contextProviders: [],
            applicationName,
            executableName: "bands.x",
        },

        /*
         *  Q2R.X
         */
        {
            content: readAssetFile(applicationName, "q2r.j2.in"),
            name: "q2r.in",
            contextProviders: [],
            applicationName,
            executableName: "q2r.x",
        },

        /*
         *  PROJWFC.X
         */
        {
            content: readAssetFile(applicationName, "projwfc.j2.in"),
            name: "projwfc.in",
            contextProviders: [],
            applicationName,
            executableName: "projwfc.x",
        },

        /*
         *  DOS.X
         */
        {
            content: readAssetFile(applicationName, "dos.j2.in"),
            name: "dos.in",
            contextProviders: [],
            applicationName,
            executableName: "dos.x",
        },

        /*
         *  PP.X
         */
        {
            content: readAssetFile(applicationName, "pp_density.j2.in"),
            name: "pp_density.in",
            contextProviders: [],
            applicationName,
            executableName: "pp.x",
        },
        {
            content: readAssetFile(applicationName, "pp_electrostatic_potential.j2.in"),
            name: "pp_electrostatic_potential.in",
            contextProviders: [],
            applicationName,
            executableName: "pp.x",
        },

        /*
         *  NEB.X
         */
        {
            content: readAssetFile(applicationName, "neb.j2.in"),
            name: "neb.in",
            contextProviders: [
                "KGridFormDataManager",
                "NEBFormDataManager",
                "QENEBInputDataManager",
                "PlanewaveCutoffDataManager",
            ],
            applicationName,
            executableName: "neb.x",
        },

        /*
         *  Sternheimer GW
         */
        {
            content: readAssetFile(applicationName, "gw_bands_plasmon_pole.j2.in"),
            name: "gw_bands_plasmon_pole.in",
            contextProviders: [
                "KGridFormDataManager",
                "QGridFormDataManager",
                "ExplicitKPath2PIBAFormDataManager",
            ],
            applicationName,
            executableName: "gw.x",
        },
        {
            content: readAssetFile(applicationName, "gw_bands_full_frequency.j2.in"),
            name: "gw_bands_full_frequency.in",
            contextProviders: [
                "KGridFormDataManager",
                "QGridFormDataManager",
                "ExplicitKPath2PIBAFormDataManager",
            ],
            applicationName,
            executableName: "gw.x",
        },

        /*
         *  AVERAGE.X
         */
        {
            content: readAssetFile(applicationName, "average.j2.in"),
            name: "average.in",
            contextProviders: [],
            applicationName,
            executableName: "average.x",
        },
    ];

    return allAssets.map((a) => makeObjectsFromContextProviderNames(a));
};
