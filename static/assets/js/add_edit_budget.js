$(document).ready(function() {
    "use strict";

    $(".budget_category_hidden").each(function() {
        if(this.value && this.value != 0) {
            $('#' + this.id + '_interface').val(this.value);
        }
    });

    update_totals(false);
    update_totals(true);

    $(".update_budget_value").change(function() {
        update_input_fields(this.id, this.value, false);
    });

    $(".update_budget_value_future").change(function() {
        update_input_fields(this.id, this.value, true);
    });

    function update_input_fields(id, value, future_values) {
        $('#'+id.replace('_interface', '')).val(value);

        if(future_values) {
            var opposite_element =
                '#'+id.replace('_future_interface', '_interface');
        } else {
            var opposite_element =
                '#'+id.replace('_interface', '_future_interface');
        }

        if(!($(opposite_element).val())) {
            $(opposite_element).val(value);
            $(opposite_element).trigger("change");
            update_totals(!future_values);
        }
        update_totals(future_values);
    }

    function update_totals(future_values) {
        var budget_types = [];
        var postfix = '';

        if(future_values) {
            postfix = '_future';
        }

        $(".update_budget_value" + postfix).each(function () {
            if (budget_types.indexOf($(this).data('budget_type')) == -1) {
                budget_types.push($(this).data('budget_type'));
            }
        });

        if (budget_types) {
            budget_types.map(function (budget_type) {
                var total = 0;

                $("." + budget_type).each(function () {
                    if (!isNaN(parseFloat(this.value))) {
                        total += parseFloat(this.value);
                    }
                });

                if (total) {
                    $("#" + budget_type + "_total").html(total.toFixed(2));
                } else {
                    $("#" + budget_type + "_total").html('-');
                }

            });
        }

        var grand_total = 0;

        $(".budget_type_total" + postfix).each(function () {
            if (!isNaN(parseFloat($(this).html()))) {
                if ($(this).data('budget_type') == 'Income') {
                    grand_total += parseFloat($(this).html());
                } else {
                    grand_total -= parseFloat($(this).html());
                }
            }
        });

        if (grand_total) {
            $("#grand_total" + postfix).html(grand_total.toFixed(2));
            if (grand_total <= 0) {
                $("#grand_total" + postfix).parent().removeClass('success');
                $("#grand_total" + postfix).parent().addClass('warning');
            } else {
                $("#grand_total" + postfix).parent().removeClass('warning');
                $("#grand_total" + postfix).parent().addClass('success');
            }
        } else {
            $("#grand_total" + postfix).parent().removeClass('warning');
            $("#grand_total" + postfix).parent().addClass('success');
            $("#grand_total" + postfix).html('-');
        }

    }

});
