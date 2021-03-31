import {makeObjectsFromContextProviderNames} from "../utils";

import INCAR from "./assets/INCAR";
import KPOINTS from "./assets/KPOINTS";
import POSCAR from "./assets/POSCAR";

import INCAR_BANDS from "./assets/INCAR_bands";
import INCAR_ZPE from "./assets/INCAR_zpe";
import INCAR_RELAX from "./assets/INCAR_relax";
import INCAR_VC_RELAX from "./assets/INCAR_vc_relax";
import _MIXIN_INCAR_HSE from "./assets/_MIXIN_INCAR_hse";

import KPOINTS_BANDS from "./assets/KPOINTS_bands";
import KPOINTS_CONV from "./assets/KPOINTS_conv";

import INCAR_NEB from "./assets/INCAR_neb";
import POSCAR_NEB_FINAL from "./assets/POSCAR_NEB_final";
import POSCAR_NEB_INITIAL from "./assets/POSCAR_NEB_inital";
import INCAR_NEB_INITIAL_FINAL from "./assets/INCAR_neb_initial_final";

const allAssets = [
    /*
     *  VASP
     */
    {
        "content": INCAR,
        "name": "INCAR",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": INCAR_BANDS,
        "name": "INCAR_BANDS",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": INCAR_ZPE,
        "name": "INCAR_ZPE",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": INCAR_RELAX,
        "name": "INCAR_RELAX",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": INCAR_VC_RELAX,
        "name": "INCAR_VC_RELAX",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": INCAR.concat(_MIXIN_INCAR_HSE),
        "name": "INCAR_HSE",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": INCAR_BANDS.concat(_MIXIN_INCAR_HSE),
        "name": "INCAR_BANDS_HSE",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },

    {
        "content": KPOINTS,
        "name": "KPOINTS",
        "contextProviders": [
            "KGridFormDataManager",
            "VASPInputDataManager",
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": KPOINTS_BANDS,
        "name": "KPOINTS_BANDS",
        "contextProviders": [
            "KPathFormDataManager",
            "VASPInputDataManager",
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": KPOINTS_CONV,
        "name": "KPOINTS_CONV",
        "contextProviders": [
            "KGridFormDataManager",
            "VASPInputDataManager",
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },

    {
        "content": POSCAR,
        "name": "POSCAR",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": INCAR_NEB,
        "name": "INCAR_NEB",
        "contextProviders": [
            "NEBFormDataManager",
            "VASPNEBInputDataManager"
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": INCAR_NEB_INITIAL_FINAL,
        "name": "INCAR_NEB_INITIAL_FINAL",
        "contextProviders": [
            "NEBFormDataManager",
            "VASPNEBInputDataManager"
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": POSCAR_NEB_INITIAL,
        "name": "POSCAR_NEB_INITIAL",
        "contextProviders": [
            "NEBFormDataManager",
            "VASPNEBInputDataManager"
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },
    {
        "content": POSCAR_NEB_FINAL,
        "name": "POSCAR_NEB_FINAL",
        "contextProviders": [
            "NEBFormDataManager",
            "VASPNEBInputDataManager"
        ],
        "applicationName": "vasp",
        "executableName": "vasp"
    },

];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
