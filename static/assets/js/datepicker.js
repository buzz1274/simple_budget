$(document).ready(function() {

    $("#id_transaction_date").datepicker({changeYear: true,
        showOn: "both",
        buttonImage: "/static/assets/img/calendar.gif",
        dateFormat: "d MM, yy",
        buttonImageOnly: true});

    var position = $('#id_transaction_date').position();
    var width = $('#id_transaction_date').outerWidth();

    $('.ui-datepicker-trigger').css({'position': 'absolute',
        'top': position.top + 7,
        'left': position.left + width + 5});
});
