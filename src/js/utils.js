import _ from "underscore";
export const makeObjectsFromContextProviderNames = (asset) => {
    return {
        ...asset,
        contextProviders: asset.contextProviders.map(name => {return _.isObject(name) ? name : {name}})
    }
};
