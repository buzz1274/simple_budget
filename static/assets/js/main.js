require.config({
    baseURL: "static/assets/js",
    paths: {
        "jquery": "//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min",
        "underscore": "//cdnjs.cloudflare.com/ajax/libs/lodash.js/2.2.1/lodash.underscore",
        "backbone": "//cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.2/backbone-min",
        "bootstrap": "//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min",
        "jquery_ui": "//code.jquery.com/ui/1.9.1/jquery-ui.min",
        "marionette": "//cdnjs.cloudflare.com/ajax/libs/backbone.marionette/2.1.0/backbone.marionette.min",
        "json2": "//cdnjs.cloudflare.com/ajax/libs/json2/20140204/json2.min"
    },
    shim: {
        "bootstrap": {
            exports: "$",
            deps: ['jquery']
        },
        "jquery_ui": {
            exports: "$",
            deps: ['jquery']
        },
        "backbone": {
            exports: "Backbone",
            deps: ["jquery", "underscore", "json2"]
        },
        "marionette": {
            exports: "Marionette",
            deps: ["backbone"]
        }
    }
});

require(["app"], function (Accounts) {
    "use strict";
    Accounts.start();
});