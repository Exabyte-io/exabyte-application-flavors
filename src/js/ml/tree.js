import monitors from "../allowed_monitors";

export default {
    train: {
        isDefault: true,
        monitors: [monitors.standard_output],
        results: ["workflow:ml_predict"],
        flavors: {
            train: {
                isDefault: true,
                input: [],
                monitors: [monitors.standard_output],
            },
        },
    },
    score: {
        isDefault: false,
        monitors: [monitors.standard_output],
        results: ["predicted_properties"],
        flavors: {
            score: {
                isDefault: true,
                input: [],
                monitors: [monitors.standard_output],
            },
        },
    },
};
