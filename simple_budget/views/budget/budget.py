from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required, user_passes_test
from simple_budget.models.transaction.transaction_category import \
    TransactionCategory
from simple_budget.models.budget.budget_category import BudgetCategory
from simple_budget.helper.date_calculation import DateCalculation
from simple_budget.helper.helper import clean_message_from_url
from simple_budget.forms.budget.add_edit_budget_form import \
    AddEditBudgetForm
from simple_budget.forms.budget.delete_budget_form import \
    DeleteBudgetForm
from simple_budget.forms.budget.add_edit_budget_category_form import \
    AddEditBudgetCategoryForm
from simple_budget.forms.budget.delete_budget_category_form import \
    DeleteBudgetCategoryForm
from simple_budget.models.budget.budget import Budget
from simple_budget.models.budget.budget_type import BudgetType


@login_required
def summary(request):
    """
    index
    """
    return render_to_response('budget/summary.html',
                              {'spending_by_budget_type':
                                   BudgetType().spending_by_budget_type()},
                              context_instance=RequestContext(request))

@login_required
def budget(request):
    """
    index
    """
    prev_month, next_month, start_date, end_date, display_date = \
        DateCalculation.calculate_dates(request.GET.get('date', None))

    if not start_date or not end_date:
        return HttpResponseRedirect('/budget/')

    transactions, totals, grand_total = \
        Budget().get_budget(start_date, end_date)

    return render_to_response('budget/budget.html',
                              {'transactions': transactions,
                               'totals': totals,
                               'grand_total': grand_total,
                               'date': display_date,
                               'next_month': next_month,
                               'prev_month': prev_month},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser,
                  login_url='/?message=no_permissions_error',
                  redirect_field_name=None)
def add_edit_budgets(request, action=None, budget_id=None):

    budget_value_error_found = False
    referer = \
        clean_message_from_url(request.META.get('HTTP_REFERER', None))
    prev_month, next_month, start_date, end_date, today = \
        DateCalculation().calculate_dates()

    transactions, totals, grand_total = \
        Budget().get_budget(start_date, end_date, budget_id)

    if request.method == 'POST':
        if request.POST.get('submit', None) != 'Submit':
            return HttpResponseRedirect(request.POST.get('referer', '/'))

        if action == 'edit':
            edit_budget = True
        else:
            edit_budget = False

        form = AddEditBudgetForm(request.POST, transactions=transactions,
                                 edit_budget=edit_budget)

        if form.is_valid():
            if Budget().add_edit_budget(action, request.POST):
                message = 'success'
            else:
                message = 'failure'

            return HttpResponseRedirect(
                '/budgets/?message=budget_%s_%s' % (action, message,))
        else:
            for transaction in transactions:
                if form['budget_category_%s' %
                        (transaction.budget_category_id,)].errors:
                    transaction.has_error = True
                    budget_value_error_found = True

    else:
        if action == 'edit' and budget_id:
            edit_budget = get_object_or_404(Budget, pk=budget_id)

            form = \
                AddEditBudgetForm(transactions=transactions,
                                  edit_budget=True,
                                  initial={'referer':
                                               referer,
                                           'budget_id':
                                               edit_budget.budget_id,
                                           'budget_name':
                                               edit_budget.budget_name,
                                           'budget_description':
                                               edit_budget.budget_description,
                                           'budget_master':
                                               edit_budget.budget_master})
        else:
            form = AddEditBudgetForm(transactions=transactions,
                                     initial={'referer': referer})

    return render_to_response('budget/add_edit_budget.html',
                              {'form': form,
                               'action': action,
                               'budget_value_error_found':
                                   budget_value_error_found,
                               'totals': totals,
                               'grand_total': grand_total,
                               'transactions': transactions},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser,
                  login_url='/?message=no_permissions_error',
                  redirect_field_name=None)
def delete_budgets(request, budget_id=None):
    """
    deletes the supplied budget category
    :param request:
    :return:
    """
    budget_to_delete = get_object_or_404(Budget, pk=budget_id)
    referer = \
        clean_message_from_url(request.META.get('HTTP_REFERER', None))

    if request.method == 'POST':
        if request.POST.get('submit', None) == 'Cancel':
            return HttpResponseRedirect(request.POST.get('referer', '/'))

        form = DeleteBudgetForm(request.POST)

        if form.is_valid():
            if budget_to_delete.delete_budget():
                return HttpResponseRedirect(
                    '/budgets/?message=budget_delete_success')
            else:
                return HttpResponseRedirect(
                    '/budgets/?message=budget_delete_failure')
    else:
        form = DeleteBudgetForm(initial={'budget_id': budget_to_delete.pk,
                                         'referer': referer})

    return render_to_response('budget/budget_delete.html',
                              {'form': form,
                               'budget_is_master':
                                   budget_to_delete.budget_master,
                               'refer': referer},
                              context_instance=RequestContext(request))

@login_required
def budgets(request, budget_id=None):
    """
    index
    """
    if budget_id:
        budget_to_view = Budget.objects.get(pk=budget_id)
    else:
        budget_to_view = None

    if not budget_id or not budget_to_view:
        return render_to_response('budget/budgets.html',
                                  {'budgets': Budget.objects.all().
                                                order_by('-budget_master')},
                                  context_instance=RequestContext(request))
    else:
        prev_month, next_month, start_date, end_date, today = \
            DateCalculation().calculate_dates()

        transactions, totals, grand_total = \
            Budget().get_budget(start_date, end_date, budget_id)

        return render_to_response('budget/budget_detail.html',
                                  {'budget': budget_to_view,
                                   'view_type': 'view',
                                   'totals': totals,
                                   'grand_total': grand_total,
                                   'transactions': transactions},
                                  context_instance=RequestContext(request))

@login_required
def category(request):
    """
    budget categories
    :param request:
    :return:
    """
    sort, budget_categories = \
        BudgetCategory.budget_categories(request.GET.get('sort', None))

    return render_to_response('budget/category.html',
                              {'budget_categories': budget_categories,
                               'sort': sort},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser,
                  login_url='/?message=no_permissions_error',
                  redirect_field_name=None)
def add_edit_budget_category(request, action, budget_category_id):
    """
    add edit budget categories
    :param request:
    :return:
    """
    referer = \
        clean_message_from_url(request.META.get('HTTP_REFERER', None))

    if request.method == 'POST':
        if request.POST.get('submit', None) != 'Submit':
            return HttpResponseRedirect(request.POST.get('referer', '/'))

        form = AddEditBudgetCategoryForm(request.POST)

        if form.is_valid():
            try:
                if form.cleaned_data['budget_category_id']:
                    budget_category = \
                        BudgetCategory(
                            budget_category_id=
                                form.cleaned_data['budget_category_id'],
                            budget_type_id=
                                form.cleaned_data['budget_type_id'],
                            budget_category=
                                form.cleaned_data['budget_category'])
                else:
                    budget_category = \
                        BudgetCategory(
                            budget_type_id=
                                form.cleaned_data['budget_type_id'],
                            budget_category=
                                form.cleaned_data['budget_category'])

                budget_category.save()

                if budget_category.pk:
                    message = 'success'
                else:
                    message = 'failure'
            except DatabaseError:
                message = 'failure'

            return HttpResponseRedirect('/budget/category/?'
                                        'message=budget_category_%s_%s'
                                        % (action, message,))

    else:
        if action == 'edit':
            budget_category = get_object_or_404(BudgetCategory,
                                                pk=budget_category_id)
            form = AddEditBudgetCategoryForm(
                initial={'referer': referer,
                         'budget_category_id':
                             budget_category.budget_category_id,
                         'budget_category':
                             budget_category.budget_category,
                         'budget_type_id':
                             budget_category.budget_type_id})
        else:
            form = AddEditBudgetCategoryForm(initial={'referer': referer})

    return render_to_response('budget/add_edit_budget_category.html',
                              {'referer': referer,
                               'form': form,
                               'action': action},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser,
                  login_url='/?message=no_permissions_error',
                  redirect_field_name=None)
def delete_budget_category(request, budget_category_id):
    """
    deletes the supplied budget category
    :param request:
    :return:
    """
    budget_category = get_object_or_404(BudgetCategory,
                                        pk=budget_category_id)
    referer = \
        clean_message_from_url(request.META.get('HTTP_REFERER', None))

    transaction_categories = \
        TransactionCategory.objects.filter(budget_category_id=
                                           budget_category_id).count()

    if request.method == 'POST':
        if request.POST.get('submit', None) == 'Cancel':
            return HttpResponseRedirect(request.POST.get('referer', '/'))

        form = \
            DeleteBudgetCategoryForm(
                request.POST,
                current_budget_category_id=budget_category_id,
                select_new_category=bool(transaction_categories))

        if form.is_valid():
            try:
                if form.cleaned_data['transfer_budget_category_id']:
                    TransactionCategory.objects.filter(budget_category_id=
                                                       budget_category_id). \
                        update(budget_category_id=
                               form.cleaned_data['transfer_budget_category_id'])

                budget_category.delete()

                return HttpResponseRedirect(
                    '/budget/category/?'
                    'message=budget_category_delete_success')
            except DatabaseError:
                return HttpResponseRedirect(
                    '/budget/category/?'
                    'message=budget_category_delete_failure')
    else:
        form = DeleteBudgetCategoryForm(
            current_budget_category_id=budget_category_id,
            initial={'budget_category_id': budget_category.pk,
                     'referer': referer})

    return render_to_response('budget/delete_budget_category.html',
                              {'form': form,
                               'transaction_categories': transaction_categories,
                               'refer': referer},
                              context_instance=RequestContext(request))