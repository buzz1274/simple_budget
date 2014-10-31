define(["accounts", "modules/accounts/views/summary_view"], function(Accounts, View) {
    "use strict";
    Accounts.module("Accounts.Summary", function(Summary, Accounts, Backbone,
                                                 Marionette, $, _) {

        Summary.Controller = {
            budgetSummaryController: function () {
                alert("SUMMARY");
            }
        }
    });
});