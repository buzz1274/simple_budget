from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from simple_budget.models.account.account import Account
from django.http import HttpResponse
import json


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

@login_required
def debt_summary(request):
    """
    index
    """
    return HttpResponse(json.dumps(Account().debt_balance_summary()),
                        content_type='application/json')