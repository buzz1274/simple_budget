from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from simple_budget.models.budget.budget_category import BudgetCategory
from simple_budget.models.budget.budget_type import BudgetType
from simple_budget.helper.date_calculation import DateCalculation


def summary(request):
    """
    budget summary
    """
    return render_to_response('budget/summary.html',
                              {'spending_by_budget_type':
                                   BudgetType().spending_by_budget_type()},
                              context_instance=RequestContext(request))

def budget(request):
    """
    index
    """
    prev_month, next_month, start_date, end_date, display_date = \
        DateCalculation.calculate_dates(request.GET.get('date', None))

    if not start_date or not end_date:
        return HttpResponseRedirect('/budget/')

    transactions, totals, grand_total = \
        BudgetCategory().spending_by_budget_category(start_date, end_date)

    return render_to_response('budget/budget.html',
                              {'transactions': transactions,
                               'totals': totals,
                               'grand_total': grand_total,
                               'date': display_date,
                               'next_month': next_month,
                               'prev_month': prev_month},
                              context_instance=RequestContext(request))