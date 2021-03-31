import _ from "underscore";

export const makeObjectsFromContextProviderNames = (asset) => {
    return {
        ...asset,
        contextProviders: asset.contextProviders.map(name => {return _.isObject(name) ? name : {name}})
    }
};

/**
 * Creates deep clone of the object.
 * @param obj {Object}
 */
export function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}
