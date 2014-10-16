define(["marionette",
        "config/marionette/regions/dialog"], function (Marionette) {
    "use strict";

    var Accounts = new Marionette.Application();

    Accounts.addRegions({
        headerRegion: "#header-region",
        mainRegion: "#main-region",
        dialogRegion: Marionette.Region.Dialog.extend({
            el: "#dialogue-region"
        })
    });

    Accounts.navigate = function(route, options) {
        options || (options = {});
        Backbone.history.navigate(route, options);
    };

    Accounts.getCurrentRoute = function() {
        return Backbone.history.fragment;
    };

    Accounts.on("start", function () {
        if(Backbone.history) {
            Backbone.history.start();

            if(this.getCurrentRoute() == "") {
                Accounts.trigger("accounts:summary");
            }

        }
    });

    return Accounts;

});