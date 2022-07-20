/**
 * build_templates uses node API to read all jinja templates from the FS
 * at build time and writes them out to a single templates.js file for
 * downstream consumption to avoid FS calls in the browser.
 */
const fs = require("fs");
const flavors = require("./lib/js/assets");
const obj = flavors.getAllAppTemplates();
fs.writeFileSync("./lib/js/templates.js", "module.exports = {allTemplates: " + JSON.stringify(obj) + "}", "utf8");

// Verify contents
// const templates = require("./lib/js/templates");
// console.log(templates);

// Downstream usage of compiled templates
// import { allTemplates } from "@exabyte-io/application-flavors/templates";
