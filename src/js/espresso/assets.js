import {makeObjectsFromContextProviderNames, readAssetFile} from "../utils";

const applicationName = "espresso";

const allAssets = [
    /*
     *  PW.X
     */
    {
        "content": readAssetFile(applicationName, "pw_scf.in.jinja2"),
        "name": "pw_scf.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "pw.x"
    },
    {
        "content": readAssetFile(applicationName, "pw_scf_bands_hse.in.jinja2"),
        "name": "pw_scf_bands_hse.in",
        "contextProviders": [
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
            "QGridFormDataManager",
            "ExplicitKPathFormDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "pw.x"
    },
    {
        "content": readAssetFile(applicationName, "pw_esm.in.jinja2"),
        "name": "pw_esm.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
            "BoundaryConditionsFormDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "pw.x"
    },
    {
        "content": readAssetFile(applicationName, "pw_esm_relax.in.jinja2"),
        "name": "pw_esm_relax.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
            "BoundaryConditionsFormDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "pw.x"
    },

    {
        "content": readAssetFile(applicationName, "pw_scf_kpt_conv.in.jinja2"),
        "name": "pw_scf_kpt_conv.in",
        "contextProviders": [
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "pw.x"
    },
    {
        "content": readAssetFile(applicationName, "pw_nscf.in.jinja2"),
        "name": "pw_nscf.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "pw.x"
    },
    {
        "content": readAssetFile(applicationName, "pw_relax.in.jinja2"),
        "name": "pw_relax.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "pw.x"
    },
    {
        "content": readAssetFile(applicationName, "pw_vc_relax.in.jinja2"),
        "name": "pw_vc_relax.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "pw.x"
    },
    {
        "content": readAssetFile(applicationName, "pw_bands.in.jinja2"),
        "name": "pw_bands.in",
        "contextProviders": [
            "KPathFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "pw.x"
    },

    /*
     *  PH.X
     */
    {
        "content": readAssetFile(applicationName, "ph_grid.in.jinja2"),
        "name": "ph_grid.in",
        "contextProviders": [
            "QGridFormDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "ph.x"
    },
    {
        "content": readAssetFile(applicationName, "ph_path.in.jinja2"),
        "name": "ph_path.in",
        "contextProviders": [
            "QPathFormDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "ph.x"
    },
    {
        "content": readAssetFile(applicationName, "ph_gamma.in.jinja2"),
        "name": "ph_gamma.in",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": "ph.x"
    },
    {
        "content": readAssetFile(applicationName, "ph_init_qpoints.in.jinja2"),
        "name": "ph_init_qpoints.in",
        "contextProviders": ["QGridFormDataManager"],
        "applicationName": applicationName,
        "executableName": "ph.x"
    },
    {
        "content": readAssetFile(applicationName, "ph_grid_restart.in.jinja2"),
        "name": "ph_grid_restart.in",
        "contextProviders": ["QGridFormDataManager"],
        "applicationName": applicationName,
        "executableName": "ph.x"
    },
    {
        "content": readAssetFile(applicationName, "ph_single_irr_qpt.in.jinja2"),
        "name": "ph_single_irr_qpt.in",
        "contextProviders": ["QGridFormDataManager"],
        "applicationName": applicationName,
        "executableName": "ph.x"
    },

    /*
     *  MATDYN.X
     */
    {
        "content": readAssetFile(applicationName, "matdyn_grid.in.jinja2"),
        "name": "matdyn_grid.in",
        "contextProviders": [
            "IGridFormDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "ph.x"
    },
    {
        "content": readAssetFile(applicationName, "matdyn_path.in.jinja2"),
        "name": "matdyn_path.in",
        "contextProviders": [
            "IPathFormDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "ph.x"
    },

    /*
     *  BANDS.X
     */
    {
        "content": readAssetFile(applicationName, "bands.in.jinja2"),
        "name": "bands.in",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": "bands.x"
    },

    /*
     *  Q2R.X
     */
    {
        "content": readAssetFile(applicationName, "q2r.in.jinja2"),
        "name": "q2r.in",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": "q2r.x"
    },

    /*
     *  PROJWFC.X
     */
    {
        "content": readAssetFile(applicationName, "projwfc.in.jinja2"),
        "name": "projwfc.in",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": "projwfc.x"
    },

    /*
     *  DOS.X
     */
    {
        "content": readAssetFile(applicationName, "dos.in.jinja2"),
        "name": "dos.in",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": "dos.x"
    },

    /*
     *  PP.X
     */
    {
        "content": readAssetFile(applicationName, "pp_density.in.jinja2"),
        "name": "pp_density.in",
        "contextProviders": [],
        "applicationName": applicationName,
        "executableName": "pp.x"
    },

    /*
     *  NEB.X
     */
    {
        "content": readAssetFile(applicationName, "neb.in.jinja2"),
        "name": "neb.in",
        "contextProviders": [
            "KGridFormDataManager",
            "NEBFormDataManager",
            "QENEBInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "neb.x"
    },

    /*
     *  Sternheimer GW
     */
    {
        "content": readAssetFile(applicationName, "gw_bands_plasmon_pole.in.jinja2"),
        "name": "gw_bands_plasmon_pole.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QGridFormDataManager",
            "ExplicitKPath2PIBAFormDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "gw.x"
    },
    {
        "content": readAssetFile(applicationName, "gw_bands_full_frequency.in.jinja2"),
        "name": "gw_bands_full_frequency.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QGridFormDataManager",
            "ExplicitKPath2PIBAFormDataManager",
        ],
        "applicationName": applicationName,
        "executableName": "gw.x"
    },

];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
