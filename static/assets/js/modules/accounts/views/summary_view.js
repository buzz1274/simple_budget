define(['app'], function(Accounts) {

    "use strict";

    Accounts.module(Accounts.summary, function(View, ContactManager, Backbone,
                                               Marionette, $, _) {

        console.log("DERP");

        View.Layout = Marionette.LayoutView.extend({
            template: "#budget-summary"
        });

    });

});