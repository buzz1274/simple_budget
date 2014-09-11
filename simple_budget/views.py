from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from models.budget_category import BudgetCategory
from models.transaction import Transaction
from forms.upload_quicken_file import UploadQuickenFile
from datetime import datetime, date
import calendar


def index(request):
    """
    index
    """
    today = date(datetime.now().year, datetime.now().month, datetime.now().day)
    start_date = date(datetime.now().year, datetime.now().month, 1)
    end_date = date(datetime.now().year, datetime.now().month,
                    calendar.monthrange(datetime.now().year,
                                        datetime.now().month)[1])

    if end_date > today:
        end_date = today

    transactions = BudgetCategory().budget_transactions(start_date, end_date)
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
                                             'date': start_date,
                                             'form': form},
                              context_instance=RequestContext(request))
