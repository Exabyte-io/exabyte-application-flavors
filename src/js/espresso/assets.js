import {makeObjectsFromContextProviderNames} from "../utils";

import PW_SCF from "./assets/pw_scf.in";
import PW_SCF_KPT_CONV from "./assets/pw_scf_kpt_conv.in";
import PW_NSCF from "./assets/pw_nscf.in";
import PW_RELAX from "./assets/pw_relax.in";
import PW_VC_RELAX from "./assets/pw_vc_relax.in";
import PW_BANDS from "./assets/pw_bands.in";

import PH_PATH from "./assets/ph_path.in";
import PH_GRID from "./assets/ph_grid.in";
import PH_GAMMA from "./assets/ph_gamma.in";
import PH_INIT_QPOINTS from "./assets/ph_init_qpoints.in";
import PH_GRID_RESTART from "./assets/ph_grid_restart.in";
import PH_SINGLE_IRR_QPT from "./assets/ph_single_irr_qpt.in";

import MATDYN_GRID from "./assets/matdyn_grid.in";
import MATDYN_PATH from "./assets/matdyn_path.in";

import Q2R from "./assets/q2r.in";

import BANDS from "./assets/bands.in";

import PROJWFC from "./assets/projwfc.in";

import DOS from "./assets/dos.in";

import PP_DENSITY from "./assets/pp_density.in";

import NEB from "./assets/neb.in";

import PW_ESM from "./assets/pw_esm.in";
import PW_ESM_RELAX from "./assets/pw_esm_relax.in";

import PW_SCF_BANDS_HSE from "./assets/pw_scf_bands_hse.in";

import GW_BANDS_PLASMON_POLE from "./assets/gw_bands_plasmon_pole.in";
import GW_BANDS_FULL_FREQUENCY from "./assets/gw_bands_full_frequency.in";

const allAssets = [
    /*
     *  PW.X
     */
    {
        "content": PW_SCF,
        "name": "pw_scf.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "pw.x"
    },
    {
        "content": PW_SCF_BANDS_HSE,
        "name": "pw_scf_bands_hse.in",
        "contextProviders": [
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
            "QGridFormDataManager",
            "ExplicitKPathFormDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "pw.x"
    },
    {
        "content": PW_ESM,
        "name": "pw_esm.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
            "BoundaryConditionsFormDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "pw.x"
    },
    {
        "content": PW_ESM_RELAX,
        "name": "pw_esm_relax.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
            "BoundaryConditionsFormDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "pw.x"
    },

    {
        "content": PW_SCF_KPT_CONV,
        "name": "pw_scf_kpt_conv.in",
        "contextProviders": [
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "pw.x"
    },
    {
        "content": PW_NSCF,
        "name": "pw_nscf.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "pw.x"
    },
    {
        "content": PW_RELAX,
        "name": "pw_relax.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "pw.x"
    },
    {
        "content": PW_VC_RELAX,
        "name": "pw_vc_relax.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "pw.x"
    },
    {
        "content": PW_BANDS,
        "name": "pw_bands.in",
        "contextProviders": [
            "KPathFormDataManager",
            "QEPWXInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "pw.x"
    },

    /*
     *  PH.X
     */
    {
        "content": PH_GRID,
        "name": "ph_grid.in",
        "contextProviders": [
            "QGridFormDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "ph.x"
    },
    {
        "content": PH_PATH,
        "name": "ph_path.in",
        "contextProviders": [
            "QPathFormDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "ph.x"
    },
    {
        "content": PH_GAMMA,
        "name": "ph_gamma.in",
        "contextProviders": [],
        "applicationName": "espresso",
        "executableName": "ph.x"
    },
    {
        "content": PH_INIT_QPOINTS,
        "name": "ph_init_qpoints.in",
        "contextProviders": ["QGridFormDataManager"],
        "applicationName": "espresso",
        "executableName": "ph.x"
    },
    {
        "content": PH_GRID_RESTART,
        "name": "ph_grid_restart.in",
        "contextProviders": ["QGridFormDataManager"],
        "applicationName": "espresso",
        "executableName": "ph.x"
    },
    {
        "content": PH_SINGLE_IRR_QPT,
        "name": "ph_single_irr_qpt.in",
        "contextProviders": ["QGridFormDataManager"],
        "applicationName": "espresso",
        "executableName": "ph.x"
    },

    /*
     *  MATDYN.X
     */
    {
        "content": MATDYN_GRID,
        "name": "matdyn_grid.in",
        "contextProviders": [
            "IGridFormDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "ph.x"
    },
    {
        "content": MATDYN_PATH,
        "name": "matdyn_path.in",
        "contextProviders": [
            "IPathFormDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "ph.x"
    },

    /*
     *  BANDS.X
     */
    {
        "content": BANDS,
        "name": "bands.in",
        "contextProviders": [],
        "applicationName": "espresso",
        "executableName": "bands.x"
    },

    /*
     *  Q2R.X
     */
    {
        "content": Q2R,
        "name": "q2r.in",
        "contextProviders": [],
        "applicationName": "espresso",
        "executableName": "q2r.x"
    },

    /*
     *  PROJWFC.X
     */
    {
        "content": PROJWFC,
        "name": "projwfc.in",
        "contextProviders": [],
        "applicationName": "espresso",
        "executableName": "projwfc.x"
    },

    /*
     *  DOS.X
     */
    {
        "content": DOS,
        "name": "dos.in",
        "contextProviders": [],
        "applicationName": "espresso",
        "executableName": "dos.x"
    },

    /*
     *  PP.X
     */
    {
        "content": PP_DENSITY,
        "name": "pp_density.in",
        "contextProviders": [],
        "applicationName": "espresso",
        "executableName": "pp.x"
    },

    /*
     *  NEB.X
     */
    {
        "content": NEB,
        "name": "neb.in",
        "contextProviders": [
            "KGridFormDataManager",
            "NEBFormDataManager",
            "QENEBInputDataManager",
            "PlanewaveCutoffDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "neb.x"
    },

    /*
     *  Sternheimer GW
     */
    {
        "content": GW_BANDS_PLASMON_POLE,
        "name": "gw_bands_plasmon_pole.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QGridFormDataManager",
            "ExplicitKPath2PIBAFormDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "gw.x"
    },
    {
        "content": GW_BANDS_FULL_FREQUENCY,
        "name": "gw_bands_full_frequency.in",
        "contextProviders": [
            "KGridFormDataManager",
            "QGridFormDataManager",
            "ExplicitKPath2PIBAFormDataManager",
        ],
        "applicationName": "espresso",
        "executableName": "gw.x"
    },

];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
