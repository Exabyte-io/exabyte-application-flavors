export default {
    name: "vasp",
    shortName: "vasp",
    summary: "Vienna Ab-initio Simulation Package",
    defaultVersion: "5.3.5",
    isLicensed: true,
    versions: [
        {
            version: "5.3.5",
            isDefault: true,
        },
        {
            version: "5.3.5",
            isDefault: false,
            build: "Non-collinear",
        },
        {
            version: "5.3.5",
            isDefault: false,
            build: "VTST",
        },
        {
            version: "5.4.4",
            isDefault: true,
        },
        {
            version: "5.4.4",
            isDefault: false,
            build: "Gamma",
        },
        {
            version: "5.4.4",
            isDefault: false,
            build: "Non-collinear",
        },
        {
            version: "5.4.4",
            isDefault: false,
            build: "VTST",
        },
        {
            version: "5.4.4",
            isDefault: false,
            build: "VTST-Gamma",
        },
        {
            version: "5.4.4",
            isDefault: false,
            build: "VTST-Non-collinear",
        },
    ],
}
