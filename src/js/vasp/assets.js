import {makeObjectsFromContextProviderNames, readAssetFile} from "../utils";

const applicationName = "vasp";
const executableName = "vasp";

const allAssets = [
    /*
     *  VASP
     */
    {
        "content": readAssetFile(applicationName, "INCAR.jinja2"),
        "name": "INCAR",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "INCAR_bands.jinja2"),
        "name": "INCAR_BANDS",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "INCAR_zpe.jinja2"),
        "name": "INCAR_ZPE",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "INCAR_relax.jinja2"),
        "name": "INCAR_RELAX",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "INCAR_vc_relax.jinja2"),
        "name": "INCAR_VC_RELAX",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "INCAR.jinja2").concat(readAssetFile(applicationName, "_MIXIN_INCAR_hse.jinja2")),
        "name": "INCAR_HSE",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "INCAR_bands.jinja2").concat(readAssetFile(applicationName, "_MIXIN_INCAR_hse.jinja2")),
        "name": "INCAR_BANDS_HSE",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },

    {
        "content": readAssetFile(applicationName, "KPOINTS.jinja2"),
        "name": "KPOINTS",
        "contextProviders": [
            "KGridFormDataManager",
            "VASPInputDataManager",
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "KPOINTS_bands.jinja2"),
        "name": "KPOINTS_BANDS",
        "contextProviders": [
            "KPathFormDataManager",
            "VASPInputDataManager",
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "KPOINTS_conv.jinja2"),
        "name": "KPOINTS_CONV",
        "contextProviders": [
            "KGridFormDataManager",
            "VASPInputDataManager",
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },

    {
        "content": readAssetFile(applicationName, "POSCAR.jinja2"),
        "name": "POSCAR",
        "contextProviders": [
            "VASPInputDataManager",
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "INCAR_neb.jinja2"),
        "name": "INCAR_NEB",
        "contextProviders": [
            "NEBFormDataManager",
            "VASPNEBInputDataManager"
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "INCAR_neb_initial_final.jinja2"),
        "name": "INCAR_NEB_INITIAL_FINAL",
        "contextProviders": [
            "NEBFormDataManager",
            "VASPNEBInputDataManager"
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "POSCAR_NEB_initial.jinja2"),
        "name": "POSCAR_NEB_INITIAL",
        "contextProviders": [
            "NEBFormDataManager",
            "VASPNEBInputDataManager"
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },
    {
        "content": readAssetFile(applicationName, "POSCAR_NEB_final.jinja2"),
        "name": "POSCAR_NEB_FINAL",
        "contextProviders": [
            "NEBFormDataManager",
            "VASPNEBInputDataManager"
        ],
        "applicationName": applicationName,
        "executableName": executableName
    },

];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
