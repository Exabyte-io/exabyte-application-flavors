import {makeObjectsFromContextProviderNames} from "../utils";

import NWChemTotalEnergy from "./assets/nwchem_total_energy.inp";

const allAssets = [
    {
        "content": NWChemTotalEnergy,
        "name": "nwchem_total_energy.inp",
        "contextProviders": [
            "NWChemInputDataManager"
        ],
        "applicationName": "nwchem",
        "executableName": "nwchem"
    }
];

export default allAssets.map(a => makeObjectsFromContextProviderNames(a));
