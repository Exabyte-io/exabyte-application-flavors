import { makeObjectsFromContextProviderNames, readAssetFile } from "../utils";

const applicationName = "vasp";
const executableName = "vasp";

// Here, we're returning a delayed-evaluation lambda, to avoid loading the asset files in scenarios where they're not
// available, like on the client.
export default () => {
    const allAssets = [
        /*
         *  VASP
         */
        {
            content: readAssetFile(applicationName, "INCAR.j2"),
            name: "INCAR",
            contextProviders: ["VASPInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "INCAR_bands.j2"),
            name: "INCAR_BANDS",
            contextProviders: ["VASPInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "INCAR_zpe.j2"),
            name: "INCAR_ZPE",
            contextProviders: ["VASPInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "INCAR_relax.j2"),
            name: "INCAR_RELAX",
            contextProviders: ["VASPInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "INCAR_vc_relax.j2"),
            name: "INCAR_VC_RELAX",
            contextProviders: ["VASPInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "INCAR.j2").concat(
                readAssetFile(applicationName, "_MIXIN_INCAR_hse.j2"),
            ),
            name: "INCAR_HSE",
            contextProviders: ["VASPInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "INCAR_bands.j2").concat(
                readAssetFile(applicationName, "_MIXIN_INCAR_hse.j2"),
            ),
            name: "INCAR_BANDS_HSE",
            contextProviders: ["VASPInputDataManager"],
            applicationName,
            executableName,
        },

        {
            content: readAssetFile(applicationName, "KPOINTS.j2"),
            name: "KPOINTS",
            contextProviders: ["KGridFormDataManager", "VASPInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "KPOINTS_bands.j2"),
            name: "KPOINTS_BANDS",
            contextProviders: ["KPathFormDataManager", "VASPInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "KPOINTS_conv.j2"),
            name: "KPOINTS_CONV",
            contextProviders: ["KGridFormDataManager", "VASPInputDataManager"],
            applicationName,
            executableName,
        },

        {
            content: readAssetFile(applicationName, "POSCAR.j2"),
            name: "POSCAR",
            contextProviders: ["VASPInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "INCAR_neb.j2"),
            name: "INCAR_NEB",
            contextProviders: ["NEBFormDataManager", "VASPNEBInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "INCAR_neb_initial_final.j2"),
            name: "INCAR_NEB_INITIAL_FINAL",
            contextProviders: ["NEBFormDataManager", "VASPNEBInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "POSCAR_NEB_initial.j2"),
            name: "POSCAR_NEB_INITIAL",
            contextProviders: ["NEBFormDataManager", "VASPNEBInputDataManager"],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "POSCAR_NEB_final.j2"),
            name: "POSCAR_NEB_FINAL",
            contextProviders: ["NEBFormDataManager", "VASPNEBInputDataManager"],
            applicationName,
            executableName,
        },
    ];

    return allAssets.map((a) => makeObjectsFromContextProviderNames(a));
};
