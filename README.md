# Introduction
This repository contains the runtime assets for the various application flavors in the Exabyte platform workflow units.

# Installation
## Javascript
```shell
npm install @exabyte-io/application-flavors.js
```


# Repo Organization
Application templates live in `assets`, with each subdirectory being the name of each application.  All files in here are considered to be Jinja2 templates (regardless of the file extension), and so each file has a `*.j2.*` name as a reminder.

The javascript library source code lives in `src/js` to make room for other language libraries in the future.

# Building, Testing, and Using in Development
With a working NPM environment, do:
```shell
 npm install
 npm test
```

To build the library's source such that you can import it from another project during development, do:
```shell
npm run prepublishOnly
```
Then you can change your importing project's `package.json` to temporarily include the file path import instead of installing from NPM:
```
"@exabyte-io/application-flavors.js": "file:/some/path/to/application-flavors",
```
Remember to revert this line to an NPM version when you're done developing.
