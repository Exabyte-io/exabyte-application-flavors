import assert from "assert"
import chai from "chai"
import {getAllAppTemplates, getAppTree, allowedResults, allowedMonitors} from "../index";

describe('allowedResults is not an empty list', () => {
    assert(Array.isArray(allowedResults))
    assert(allowedResults.length > 0)
});

describe('allowedMonitors is not an empty object', () => {
    assert(allowedMonitors instanceof Object)
    assert(Object.keys(allowedMonitors).length > 0)
});

describe('Every element in ALL_INPUT_TEMPLATES is an object with the required keys', () => {
    const ALL_INPUT_TEMPLATES = getAllAppTemplates()
    assert(Array.isArray(ALL_INPUT_TEMPLATES))
    assert(ALL_INPUT_TEMPLATES.length > 0)
    ALL_INPUT_TEMPLATES.forEach( function(template, index) {
        assert('applicationName' in template)
        assert('executableName' in template)
        assert('name' in template)
        assert('content' in template)
    });
});

describe('getAppTree returns results', () => {
    const tree = getAppTree("nwchem")
    assert('nwchem' in tree)
});

describe('getAppTree raises on unknown application', () => {
    chai.expect(
        () => {getAppTree("unknown_app")}
        ).to.throw("unknown_app is not a known application with a tree.");
});
