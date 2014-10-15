from django.shortcuts import render_to_response
from django.template import RequestContext
from simple_budget.models.budget.budget_type import BudgetType
import json

def index(request):
    """
    index
    """
    return render_to_response('index.html',
                              {'spending_by_budget_type':
                                   BudgetType().spending_by_budget_type()},
                              context_instance=RequestContext(request))
