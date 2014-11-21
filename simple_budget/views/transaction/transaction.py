from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.db import DatabaseError
from simple_budget.models.transaction.transaction_category import \
    TransactionCategory
from simple_budget.forms.add_edit_transaction_category import \
    AddEditTransactionCategory
from simple_budget.models.transaction.transaction import Transaction
from simple_budget.models.transaction.transaction_line import TransactionLine
from simple_budget.forms.transaction.upload_quicken_file import \
    UploadQuickenFile
from simple_budget.forms.transaction.add_edit_transaction import \
    AddEditTransactionForm
from simple_budget.forms.transaction.delete_transaction import \
    DeleteTransactionForm
from simple_budget.models.qif_parser.qif_parser import QIFParser
from simple_budget.helper.date_calculation import DateCalculation
from simple_budget.helper.helper import clean_message_from_url
from django.conf import settings
import json


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
        if request.POST.get('submit', None) == 'Cancel':
            return HttpResponseRedirect(request.POST.get('referer', '/'))

        form = AddEditTransactionForm(request.POST)

        if form.is_valid():
            try:
                Transaction().add_edit_transaction(action, form.cleaned_data)
                return HttpResponseRedirect(
                    '/transactions/?message=%s_success' % (message,))
            except DatabaseError:
                return HttpResponseRedirect(
                    '/transactions/?message=%s_failure' % (message,))

    else:
        referer = \
            clean_message_from_url(request.META.get('HTTP_REFERER', None))

        if action == 'edit':
            form = AddEditTransactionForm(
                initial={'referer':
                             referer,
                         'transaction_line_id':
                             transaction_line.pk,
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

def category(request):
    """
    displays transaction category --> budget category mapping
    """
    sort, transaction_categories = \
        TransactionCategory.transaction_category_mapping(request.GET.get('sort', None))

    return render_to_response('transaction/category.html',
                              {'sort': sort,
                               'transaction_categories': transaction_categories},
                              context_instance=RequestContext(request))

def upload_quicken_file(request):
    """
    processes an uploaded quicken file
    """
    if not settings.QUICKEN_IMPORT_ACTIVE:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        print request.POST.get('submit', None)
        if request.POST.get('submit', None) == 'Cancel':
            print request.POST.get('referer', '/')
            return HttpResponseRedirect(request.POST.get('referer', '/'))

        form = UploadQuickenFile(request.POST, request.FILES)
        if form.is_valid():
            if Transaction.process_upload_quicken_file(request.FILES['file']):
                return HttpResponseRedirect('/budget/?message=upload_success')
            else:
                return HttpResponseRedirect('/budget/?message=upload_failure')

    else:
        referer = \
            clean_message_from_url(request.META.get('HTTP_REFERER', None))
        form = UploadQuickenFile(initial={'referer': referer})

    return render_to_response('transaction/upload_quicken_file.html',
                              {'form': form},
                              context_instance=RequestContext(request))

def upload_quicken_file_status(request):
    """
    gets the status for the last uploaded qif file
    :return:
    """
    return HttpResponse(json.dumps({'status':  QIFParser.get_status()}),
                        content_type='application/json')

def add_edit_transaction_category(request, action, transaction_category_id=None):
    """
    adds/edits budget category
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = AddEditTransactionCategory(request.POST)
        if form.is_valid():
            if form.cleaned_data['transaction_category_id']:
                transaction_category = \
                    TransactionCategory(transaction_category_id=
                                            form.cleaned_data['transaction_category_id'],
                                        budget_category_id=
                                            form.cleaned_data['budget_category'],
                                        transaction_category=
                                            form.cleaned_data['transaction_category'])
            else:
                transaction_category = \
                    TransactionCategory(budget_category_id=
                                            form.cleaned_data['budget_category'],
                                        transaction_category=
                                            form.cleaned_data['transaction_category'])

            transaction_category.save()

            if transaction_category.pk:
                message = 'success'
            else:
                message = 'failure'

            return HttpResponseRedirect('/transaction/category/?'
                                        'message=transaction_category_%s_%s'
                                        % (action, message,))

    else:
        if action == 'edit' and transaction_category_id:
            transaction_category = TransactionCategory.objects.get(
                transaction_category_id=transaction_category_id)
            form = AddEditTransactionCategory(
                initial={'transaction_category_id':
                             transaction_category.transaction_category_id,
                         'transaction_category':
                            transaction_category.transaction_category,
                         'budget_category':
                             transaction_category.budget_category_id})
        else:
            form = AddEditTransactionCategory()

    return render_to_response('transaction/add_edit_transaction_category.html',
                              {'form': form},
                              context_instance=RequestContext(request))

def delete_transaction_category(request, transaction_category_id):
    """
    deletes the supplied transaction category
    :param request:
    :return:
    """
    category_to_delete = TransactionCategory.objects.get(transaction_category_id=
                                                         transaction_category_id)

    if not category_to_delete:
        message = 'invalid_transaction_category'
    else:
        try:
            category_to_delete.delete()
            message = 'transaction_category_deleted'
        except AssertionError:
            message = 'invalid_transaction_category'

    return HttpResponseRedirect('/transaction/category/?message=%s' % (message,),)