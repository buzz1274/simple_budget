from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from simple_budget.models.account.account import Account


@login_required
def debt(request):
    """
    index
    """
    debts, totals = Account().debt()

    return render_to_response('account/debt.html',
                              {'debts': debts,
                               'totals': totals},
                              context_instance=RequestContext(request))