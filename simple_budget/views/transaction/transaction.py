from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required, user_passes_test
from simple_budget.models.transaction.transaction_category import \
    TransactionCategory
from simple_budget.forms.transaction.add_edit_transaction_category_form import \
    AddEditTransactionCategoryForm
from simple_budget.forms.transaction.delete_transaction_category_form import \
    DeleteTransactionCategoryForm
from simple_budget.models.transaction.transaction import Transaction
from simple_budget.models.transaction.transaction_line import TransactionLine
from simple_budget.forms.transaction.upload_quicken_file_form import \
    UploadQuickenFileForm
from simple_budget.forms.transaction.add_edit_transaction_form import \
    AddEditTransactionForm
from simple_budget.forms.transaction.delete_transaction_form import \
    DeleteTransactionForm
from simple_budget.models.transaction.qif_parser import QIFParser
from simple_budget.helper.date_calculation import DateCalculation
from simple_budget.helper.helper import clean_message_from_url
from django.conf import settings
import json


@login_required
def transactions(request):
    """
    display transaction log
    """
    prev_month, next_month, start_date, end_date, today = \
        DateCalculation.calculate_dates(request.GET.get('date', None))

    sort, monthly_transactions = \
        TransactionLine.transaction_lines(start_date, end_date,
                                          request.GET.get('sort', None))

    return render_to_response('transaction/transactions.html',
                              {'date': today,
                               'sort': sort,
                               'next_month': next_month,
                               'prev_month': prev_month,
                               'transactions': monthly_transactions},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser,
                  login_url='/?message=no_permissions_error',
                  redirect_field_name=None)
def add_edit_transaction(request, action, transaction_line_id):
    """
    add/edit a transaction
    :param request:
    :return:
    """
    if action == 'edit':
        message = 'transaction_edit'
        transaction_line = get_object_or_404(TransactionLine,
                                             pk=transaction_line_id)
    else:
        message = 'transaction_add'

    if request.method == 'POST':
        if request.POST.get('submit', None) != 'Submit':
            return HttpResponseRedirect(request.POST.get('referer', '/'))

        form = AddEditTransactionForm(request.POST)

        if form.is_valid():
            referer = request.POST.get('referer', '/transactions/?date=')

            try:
                Transaction().add_edit_transaction(action, form.cleaned_data)
                return HttpResponseRedirect(
                    '%s&message=%s_success' % (referer, message,))
            except DatabaseError:
                return HttpResponseRedirect(
                    '%s&message=%s_failure' % (referer, message,))

    else:
        referer = \
            clean_message_from_url(request.META.get('HTTP_REFERER', None))

        if action == 'edit':
            form = AddEditTransactionForm(
                initial={'referer':
                             referer,
                         'transaction_line_id':
                             transaction_line.pk,
                         'account_id':
                             transaction_line.transaction.account_id,
                         'transaction_category_id':
                             transaction_line.transaction_category_id,
                         'transaction_date':
                             transaction_line.transaction.transaction_date,
                         'amount':
                             transaction_line.amount})
        else:
            form = AddEditTransactionForm(
                initial={'referer': referer})

    return render_to_response('transaction/add_edit_transaction.html',
                {'form': form,
                 'action': action},
                context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser,
                  login_url='/?message=no_permissions_error',
                  redirect_field_name=None)
def delete_transaction(request, transaction_line_id):
    """
    deletes the supplied transaction
    :param request:
    :return:
    """
    transaction_line = get_object_or_404(TransactionLine,
                                         pk=transaction_line_id)
    referer = \
        clean_message_from_url(request.META.get('HTTP_REFERER', None))

    if request.method == 'POST':
        if request.POST.get('submit', None) == 'Cancel':
            return HttpResponseRedirect(request.POST.get('referer', '/'))

        form = DeleteTransactionForm(request.POST)

        if form.is_valid():
            try:
                Transaction().delete_transaction(form.cleaned_data)
                return HttpResponseRedirect(
                    '/transactions/?message=transaction_delete_success')
            except DatabaseError:
                return HttpResponseRedirect(
                    '/transactions/?message=transaction_delete_failure')


    form = DeleteTransactionForm(
        initial={'transaction_line_id': transaction_line.pk,
                 'referer': referer})

    return render_to_response('transaction/delete_transaction.html',
                              {'form': form,
                               'refer': referer},
                              context_instance=RequestContext(request))

@login_required
def category(request):
    """
    displays transaction category --> budget category mapping
    """
    budget_category_id = request.GET.get('bc', None)
    sort, transaction_categories = \
        TransactionCategory.transaction_category_mapping(
            request.GET.get('sort', None), budget_category_id)

    return render_to_response('transaction/category.html',
                              {'sort': sort,
                               'budget_category_id': budget_category_id,
                               'transaction_categories': transaction_categories},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser,
                  login_url='/?message=no_permissions_error',
                  redirect_field_name=None)
def add_edit_transaction_category(request, action,
                                  transaction_category_id=None):
    """
    adds/edits budget category
    :param request:
    :return:
    """
    referer = \
        clean_message_from_url(request.META.get('HTTP_REFERER', None))

    if transaction_category_id:
        transaction_category_has_children = \
            bool(TransactionCategory.objects.filter(
                transaction_category_parent_id=transaction_category_id))
    else:
        transaction_category_has_children = None

    if request.method == 'POST':
        if request.POST.get('submit', None) == 'Cancel':
            return HttpResponseRedirect(request.POST.get('referer', '/'))

        form = AddEditTransactionCategoryForm(request.POST)
        if form.is_valid():
            try:
                if form.cleaned_data['transaction_category_id']:
                    transaction_category = \
                        TransactionCategory(
                            transaction_category_id=
                                form.cleaned_data['transaction_category_id'],
                            transaction_category_parent_id=
                                form.cleaned_data['transaction_category_parent_id'],
                            budget_category_id=
                                form.cleaned_data['budget_category'],
                            transaction_category=
                                form.cleaned_data['transaction_category'])
                else:
                    transaction_category = \
                        TransactionCategory(
                            transaction_category_parent_id=
                                form.cleaned_data['transaction_category_parent_id'],
                            budget_category_id=
                                form.cleaned_data['budget_category'],
                            transaction_category=
                                form.cleaned_data['transaction_category'])

                transaction_category.save()

                if transaction_category.pk:
                    message = 'success'
                else:
                    message = 'failure'
            except DatabaseError:
                message = 'failure'

            return HttpResponseRedirect('/transaction/category/?'
                                        'message=transaction_category_%s_%s'
                                        % (action, message,))

    else:
        if action == 'edit' and transaction_category_id:
            transaction_category = get_object_or_404(TransactionCategory,
                                                     pk=transaction_category_id)
            form = AddEditTransactionCategoryForm(
                initial={'referer': referer,
                         'transaction_category_id':
                             transaction_category.transaction_category_id,
                         'transaction_category_parent_id':
                             transaction_category.transaction_category_parent_id,
                         'transaction_category':
                            transaction_category.transaction_category,
                         'budget_category':
                             transaction_category.budget_category_id})

        else:
            form = AddEditTransactionCategoryForm(initial={'referer': referer})

    return render_to_response('transaction/add_edit_transaction_category.html',
                              {'form': form,
                               'action': action,
                               'transaction_category_has_children':
                                   transaction_category_has_children},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser,
                  login_url='/?message=no_permissions_error',
                  redirect_field_name=None)
def delete_transaction_category(request, transaction_category_id):
    """
    deletes the supplied transaction category
    :param request:
    :return:
    """
    transaction_category = get_object_or_404(TransactionCategory,
                                         pk=transaction_category_id)
    referer = \
        clean_message_from_url(request.META.get('HTTP_REFERER', None))

    transaction_lines = \
        TransactionLine.objects.filter(transaction_category_id=
                                       transaction_category_id).count()

    transaction_category_children = \
        bool(TransactionCategory.objects.filter(
                transaction_category_parent_id=transaction_category_id).count())

    if request.method == 'POST':
        if (request.POST.get('submit', None) == 'Cancel' or
            transaction_category_children):
            return HttpResponseRedirect(request.POST.get('referer', '/'))

        form = \
            DeleteTransactionCategoryForm(
                request.POST,
                current_tc_id=transaction_category_id,
                select_new_category=bool(transaction_lines))

        if form.is_valid():
            try:
                if form.cleaned_data['transfer_transaction_category_id']:
                    TransactionLine.objects.filter(transaction_category_id=
                                                   transaction_category_id).\
                    update(transaction_category_id=
                           form.cleaned_data['transfer_transaction_category_id'])

                transaction_category.delete()

                return HttpResponseRedirect(
                    '/transaction/category/?'
                    'message=transaction_category_delete_success')
            except DatabaseError:
                return HttpResponseRedirect(
                    '/transaction/category/?'
                    'message=transaction_category_delete_failure')
    else:
        form = DeleteTransactionCategoryForm(
            current_tc_id=transaction_category_id,
            initial={'transaction_category_id': transaction_category.pk,
                     'referer': referer})

    return render_to_response('transaction/delete_transaction_category.html',
                              {'form': form,
                               'transaction_lines': transaction_lines,
                               'transaction_category_children':
                                    transaction_category_children,
                               'refer': referer},
                              context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser,
                  login_url='/?message=no_permissions_error',
                  redirect_field_name=None)
def upload_quicken_file(request):
    """
    processes an uploaded quicken file
    """
    if not settings.QUICKEN_IMPORT_ACTIVE:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        if request.POST.get('submit', None) == 'Cancel':
            return HttpResponseRedirect(request.POST.get('referer', '/'))

        form = UploadQuickenFileForm(request.POST, request.FILES)
        if form.is_valid():
            if Transaction.process_upload_quicken_file(request.FILES['file']):
                return HttpResponseRedirect('/budget/?message=upload_success')
            else:
                return HttpResponseRedirect('/budget/?message=upload_failure')

    else:
        referer = \
            clean_message_from_url(request.META.get('HTTP_REFERER', None))
        form = UploadQuickenFileForm(initial={'referer': referer})

    return render_to_response('transaction/upload_quicken_file.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required
def upload_quicken_file_status(request):
    """
    gets the status for the last uploaded qif file
    :return:
    """
    return HttpResponse(json.dumps({'status':  QIFParser.get_status()}),
                        content_type='application/json')