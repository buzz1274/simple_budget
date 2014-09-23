from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from models.budget_category import BudgetCategory
from models.transaction import Transaction
from forms.upload_quicken_file import UploadQuickenFile
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from settings import START_DATE
import calendar


def index(request):
    """
    index
    """
    year_month = request.GET.get('date', None)
    display_date = datetime.now()
    start_date = None
    end_date = None
    prev_month = date(datetime.now().year, datetime.now().month - 1, 1)
    next_month = date(datetime.now().year, datetime.now().month + 1, 1)

    if year_month:
        try:
            year_month = datetime.strptime(year_month, '%Y-%m')
        except ValueError:
            year_month = None

        if year_month:
            start_date = date(year_month.year, year_month.month, 1)
            if (START_DATE and
                (datetime.strptime(str(start_date), '%Y-%m-%d') <
                 datetime.strptime(START_DATE, '%Y-%m-%d')) or
                (datetime.strptime(str(start_date), '%Y-%m-%d') >
                 datetime.now())):
                start_date = None
            else:
                display_date = start_date
                end_date = date(year_month.year, year_month.month,
                calendar.monthrange(year_month.year,
                                    year_month.month)[1])
                next_month = date(year_month.year, year_month.month, 1) + \
                             relativedelta(months=1)
                prev_month = date(year_month.year, year_month.month, 1) - \
                             relativedelta(months=1)

    if (START_DATE and
        datetime.strptime(str(prev_month), '%Y-%m-%d') <
        datetime.strptime(START_DATE, '%Y-%m-%d')):
        prev_month = None

    if next_month > date(datetime.now().year, datetime.now().month,
                         datetime.now().day):
        next_month = None

    transactions, totals, grand_total = \
        BudgetCategory().budget_transactions(start_date, end_date)

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
                                             'grand_total': grand_total,
                                             'date': display_date,
                                             'next_month': next_month,
                                             'prev_month': prev_month,
                                             'form': form},
                              context_instance=RequestContext(request))
