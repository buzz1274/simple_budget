from django.shortcuts import render_to_response
from django.template import RequestContext
from simple_budget.models.budget.budget_category import BudgetCategory
from simple_budget.models.qif_parser.qif_parser import QIFParser
from simple_budget.helper.message import Message
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from simple_budget.settings import START_DATE
from simple_budget.models.budget.budget_type import BudgetType
import calendar

def summary(request):
    """
    budget summary
    """
    return render_to_response('budget/summary.html',
                              {'spending_by_budget_type':
                                   BudgetType().spending_by_budget_type()},
                              context_instance=RequestContext(request))

def budget(request):
    """
    index
    """
    year_month = request.GET.get('date', None)
    display_date = datetime.now()
    start_date = None
    end_date = None
    prev_month = date(datetime.now().year, datetime.now().month - 1, 1)
    next_month = date(datetime.now().year, datetime.now().month + 1, 1)

    if QIFParser.get_status() == 'in_progress':
        message_key, message, message_type = \
            Message().get_message('in_progress_quicken_file')
    else:
        message_key, message, message_type = \
            Message().get_message(request.GET.get('message', None))

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
        BudgetCategory().spending_by_budget_category(start_date, end_date)

    return render_to_response('budget/budget.html',
                              {'transactions': transactions,
                               'totals': totals,
                               'grand_total': grand_total,
                               'date': display_date,
                               'next_month': next_month,
                               'prev_month': prev_month,
                               'message_key': message_key,
                               'message': message,
                               'message_type': message_type},
                              context_instance=RequestContext(request))