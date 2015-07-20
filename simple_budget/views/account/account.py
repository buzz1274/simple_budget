from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from simple_budget.models.account.account import Account
from django.http import HttpResponse
import json
import collections


@login_required
def accounts(request):
    """
    summary of all accounts
    """
    all_accounts = Account().accounts()
    summary = collections.OrderedDict()
    grand_total = 0

    for account in all_accounts:
        grand_total += account.balance
        if account.account_type not in summary:
            summary[account.account_type] = account.balance
        else:
            summary[account.account_type] += account.balance

    return render_to_response('account/accounts.html',
                              {'accounts': all_accounts,
                               'grand_total': grand_total,
                               'summary': summary},
                              context_instance=RequestContext(request))

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