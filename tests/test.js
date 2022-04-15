import assert from "assert";
import { expect } from "chai";

import {
    allowedMonitors,
    allowedResults,
    getAllAppTemplates,
    getAppTree,
    getAppData,
} from "../src/js/index";

describe("allowedResults", () => {
    it("should not be empty", () => {
        assert(Array.isArray(allowedResults));
        assert(allowedResults.length > 0);
    });
});

describe("allowedMonitors", () => {
    it("should not be empty", () => {
        assert(allowedMonitors instanceof Object);
        assert(Object.keys(allowedMonitors).length > 0);
    });
});

describe("ALL_INPUT_TEMPLATES", () => {
    const ALL_INPUT_TEMPLATES = getAllAppTemplates();
    assert(Array.isArray(ALL_INPUT_TEMPLATES));
    assert(ALL_INPUT_TEMPLATES.length > 0);
    it("has all required keys in each element", () => {
        ALL_INPUT_TEMPLATES.forEach((template) => {
            assert("applicationName" in template);
            assert("executableName" in template);
            assert("name" in template);
            assert("content" in template);
        });
    });
});

describe("getAppTree", () => {
    it("returns results", () => {
        const tree = getAppTree("nwchem");
        assert("nwchem" in tree);
    });
    it("raises on unknown application", () => {
        expect(() => {
            getAppTree("unknown_app");
        }).to.throw("unknown_app is not a known application with a tree.");
    });
});

describe("getAppData", () => {
    it("returns results", () => {
        const data = getAppData("nwchem");
        assert("name" in data);
        assert(data.name === "nwchem");
    });
    it("raises on unknown application", () => {
        expect(() => {
            getAppData("unknown_app");
        }).to.throw("unknown_app is not a known application with data.");
    });
});
