export default {
    name: "vasp",
    shortName: "vasp",
    summary: "Vienna Ab-initio Simulation Package",
    defaultVersion: "5.3.5",
    versions: [
        {
            version: "5.3.5",
            isDefault: true,
            isLicensed: true,
        },
        {
            version: "5.3.5",
            isDefault: false,
            isLicensed: true,
            build: "Non-collinear",
        },
        {
            version: "5.3.5",
            isDefault: false,
            isLicensed: true,
            build: "VTST",
        },
        {
            version: "5.4.4",
            isDefault: true,
            isLicensed: true,
        },
        {
            version: "5.4.4",
            isDefault: false,
            isLicensed: true,
            build: "Gamma",
        },
        {
            version: "5.4.4",
            isDefault: false,
            isLicensed: true,
            build: "Non-collinear",
        },
        {
            version: "5.4.4",
            isDefault: false,
            isLicensed: true,
            build: "VTST",
        },
        {
            version: "5.4.4",
            isDefault: false,
            isLicensed: true,
            build: "VTST-Gamma",
        },
        {
            version: "5.4.4",
            isDefault: false,
            isLicensed: true,
            build: "VTST-Non-collinear",
        },
    ],
}
