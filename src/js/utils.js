import fs from "fs";
import path from "path";
import _ from "underscore";

export const makeObjectsFromContextProviderNames = (asset) => {
    return {
        ...asset,
        contextProviders: asset.contextProviders.map((name) => {
            return _.isObject(name) ? name : { name };
        }),
    };
};

/**
 * Creates deep clone of the object.
 * @param obj {Object}
 */
export function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

/**
 * Load an asset file for the given application, of the given name.
 * @param applicationPath {str} The directory path in the /assets directory of this package, for this application
 * @param filename {str} The name of the file in the applicationPath directory to load and return
 * @returns {str} The contents of the given file
 */
export function readAssetFile(applicationPath, filename) {
    const assetsDir = path.resolve(__dirname, "../../assets/");
    return fs.readFileSync(path.resolve(assetsDir, applicationPath, filename), "utf8");
}
