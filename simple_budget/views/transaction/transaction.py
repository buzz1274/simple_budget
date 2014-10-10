from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from simple_budget.models.transaction_category import TransactionCategory
from simple_budget.forms.add_edit_transaction_category import AddEditTransactionCategory


def index(request):
    """
    displays budget category --> quicken mapping
    """
    return render_to_response('transaction/category.html',
                              {'transaction_categories':
                                   TransactionCategory().transaction_category_mapping()},
                              context_instance=RequestContext(request))

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
    category = TransactionCategory.objects.get(transaction_category_id=
                                               transaction_category_id)

    if not category:
        message = 'invalid_transaction_category'
    else:
        try:
            category.delete()
            message = 'transaction_category_deleted'
        except AssertionError:
            message = 'invalid_transaction_category'

    return HttpResponseRedirect('/transaction/category/?message=%s' % (message,))