import {makeObjectsFromContextProviderNames, readAssetFile} from "../utils";

const applicationName = "nwchem"
const executableName = "nwchem"

const allAssets = [
    {
        "content": readAssetFile(applicationName, "nwchem_total_energy.j2.inp"),
        "name": "nwchem_total_energy.inp",
        "contextProviders": [
            "NWChemInputDataManager"
        ],
        "applicationName": applicationName,
        "executableName": executableName
    }
];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
