({
    out: "bundles/bundle.js",
    include: ["../bundle-config"],
    insertRequire: ["../bundle-config"],
    name: "almond",
    mainConfigFile: 'main.js',
    wrap: {
        startFile: "VERSION.txt",
        endFile: "patternslib/src/wrap-end.js"
    },
    optimize: "none",
    paths: {
        "almond":                      "bower_components/almond/almond"
    }
})
