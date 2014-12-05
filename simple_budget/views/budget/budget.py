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
from simple_budget.forms.budget.add_edit_budget_category_form import \
    AddEditBudgetCategoryForm
from simple_budget.forms.budget.delete_budget_category_form import \
    DeleteBudgetCategoryForm


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
        BudgetCategory().spending_by_budget_category(start_date, end_date)

    return render_to_response('budget/budget.html',
                              {'transactions': transactions,
                               'totals': totals,
                               'grand_total': grand_total,
                               'date': display_date,
                               'next_month': next_month,
                               'prev_month': prev_month},
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
            print form.cleaned_data['budget_category_id']
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
            except DatabaseError, e:
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

                    print form.cleaned_data['transfer_budget_category_id']

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