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
    account_balances = Account().account_balance_summary('debt')
    data = []

    if account_balances:
        for account_balance in account_balances:
            print account_balance
            data.append({'date': account_balance.account_balance_date.strftime('%Y-%m-%d'),
                         'balance': str(account_balance.balance)})

        print data

    return HttpResponse(json.dumps(data), content_type='application/json')