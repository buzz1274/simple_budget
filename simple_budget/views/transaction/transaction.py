from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from simple_budget.models.transaction.transaction_category import TransactionCategory
from simple_budget.forms.add_edit_transaction_category import AddEditTransactionCategory
from simple_budget.models.transaction.transaction import Transaction
from simple_budget.models.transaction.transaction_line import TransactionLine
from simple_budget.forms.upload_quicken_file import UploadQuickenFile
from simple_budget.models.qif_parser.qif_parser import QIFParser
import json
from datetime import datetime


def transactions(request):
    """
    display transaction log
    """
    display_date = datetime.now()
    monthly_transactions = TransactionLine.objects.filter(
                                transaction__transaction_date__year=2014,
                                transaction__transaction_date__month=11).\
                                order_by('transaction__transaction_date',
                                         '-amount')

    return render_to_response('transaction/transactions.html',
                              {'date': display_date,
                               'transactions': monthly_transactions},
                              context_instance=RequestContext(request))

def category(request):
    """
    displays transaction category --> budget category mapping
    """
    return render_to_response('transaction/category.html',
                              {'transaction_categories':
                                   TransactionCategory.transaction_category_mapping()},
                              context_instance=RequestContext(request))

def upload_quicken_file(request):
    """
    processes an uploaded quicken file
    """
    if request.method == 'POST':
        form = UploadQuickenFile(request.POST, request.FILES)
        if form.is_valid():
            if Transaction.process_upload_quicken_file(request.FILES['file']):
                return HttpResponseRedirect('/budget/?message=upload_success')
            else:
                return HttpResponseRedirect('/budget/?message=upload_failure')

    else:
        form = UploadQuickenFile()

    return render_to_response('transaction/upload_quicken_file.html',
                              {'form': form},
                              context_instance=RequestContext(request))

def upload_quicken_file_status():
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

    return HttpResponseRedirect('/transaction/category/?message=%s' % (message,))