var Accounts = new Marionette.Application();

Accounts.addRegions({
    mainRegion: "#main"
});

Accounts.StaticView = Marionette.ItemView.extend({
    template: "#static-template"
});

Accounts.on("start", function () {
    "use strict";
    var staticView = new Accounts.StaticView();
    Accounts.mainRegion.show(staticView);
});

Accounts.start();