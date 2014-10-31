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

    Accounts.router = Marionette.AppRouter.extend({
        appRoutes: {
            "#": "budgetSummary"
        }
    });

    var API = {
        budgetSummary: function() {
            alert("HEREW");
            require(["modules/accounts/controller/summary_controller"],
                function(budgetSummaryController) {
                    alert("DERP");
                    budgetSummaryController.Summary();
                }
            );
        }
    }

    Accounts.addInitializer(function() {
        new Accounts.router({
            controller: API
        });
    });

    console.log(Accounts);


    return Accounts;

});