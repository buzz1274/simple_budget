from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import (authenticate, login as auth_login,
                                 logout as auth_logout)
from django.contrib.auth.decorators import login_required
from simple_budget.forms.login_form import LoginForm
from django.http import HttpResponseRedirect
from simple_budget.models.budget.budget_type import BudgetType

@login_required
def index(request):
    """
    index
    """
    return render_to_response('index.html',
                              {'spending_by_budget_type':
                                   BudgetType().spending_by_budget_type()},
                              context_instance=RequestContext(request))

def logout(request):
    """
    login view
    @author David Exelby <david@sulaco.co.uk>
    """
    auth_logout(request)
    return HttpResponseRedirect('/login/?message=logged_out')

def login(request):
    """
    login form
    """
    invalid_credentials = False

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username', None),
                            password=request.POST.get('password', None))

        if user is not None and user.is_active:
            auth_login(request, user)
            request.session.set_expiry(900)
            return HttpResponseRedirect(request.POST.get('next', '/'))
        else:
            invalid_credentials = True

        form = LoginForm(request.POST)
    else:
        form = LoginForm(initial={'next': request.GET.get('next', '/')})

    return render_to_response('login.html',
                              {'form': form,
                               'invalid_credentials': invalid_credentials},
                              context_instance=RequestContext(request))
