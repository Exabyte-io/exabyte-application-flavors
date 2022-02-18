import { makeObjectsFromContextProviderNames, readAssetFile } from "../utils";

const applicationName = "nwchem";
const executableName = "nwchem";

// Here, we're returning a delayed-evaluation lambda, to avoid loading the asset files in scenarios where they're not
// available, like on the client.
export default () => {
    const allAssets = [
        {
            content: readAssetFile(applicationName, "nwchem_total_energy.j2.inp"),
            name: "nwchem_total_energy.inp",
            contextProviders: ["NWChemInputDataManager"],
            applicationName,
            executableName,
        },
    ];

    return allAssets.map((a) => makeObjectsFromContextProviderNames(a));
};
