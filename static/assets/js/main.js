$(document).ready(function() {
    "use strict";

    if(['login'].indexOf(window.location.pathname.replace(/\//g, '')) == -1) {
        setInterval(function() {
            $.ajax( "/check_auth", function() {
            }).fail(function() {
                window.location.href = '/login';
            });
        }, (17 * 60 * 1000));
    }

});