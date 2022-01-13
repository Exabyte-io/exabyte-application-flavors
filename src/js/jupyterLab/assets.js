import { makeObjectsFromContextProviderNames, readAssetFile } from "../utils";

const applicationName = "jupyterLab";
const executableName = "jupyter";

// Here, we're returning a delayed-evaluation lambda, to avoid loading the asset files in scenarios where they're not
// available, like on the client.
export default () => {
    const allAssets = [
        {
            content: readAssetFile(applicationName, "install.j2.sh"),
            name: "install.sh",
            contextProviders: [],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "configure.pyi"),
            name: "config.py",
            contextProviders: [],
            applicationName,
            executableName,
        },
        {
            content: readAssetFile(applicationName, "configure.j2.sh"),
            name: "configure.sh",
            contextProviders: [],
            applicationName,
            executableName,
        },
    ];

    return allAssets.map((a) => makeObjectsFromContextProviderNames(a));
};
