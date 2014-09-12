from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from models.budget_category import BudgetCategory
from models.transaction import Transaction
from forms.upload_quicken_file import UploadQuickenFile
from datetime import datetime


def index(request):
    """
    index
    """
    transactions = BudgetCategory().budget_transactions()
    totals = BudgetCategory().calculate_totals(transactions)

    if request.method == 'POST':
        form = UploadQuickenFile(request.POST, request.FILES)
        if form.is_valid():
            if Transaction.process_upload_quicken_file(request.FILES['file']):
                return HttpResponseRedirect('/?message=upload_success')
            else:
                return HttpResponseRedirect('/?message=upload_failure')

    else:
        form = UploadQuickenFile()

    return render_to_response('index.html', {'transactions': transactions,
                                             'totals': totals,
                                             'date': datetime.now(),
                                             'form': form},
                              context_instance=RequestContext(request))
