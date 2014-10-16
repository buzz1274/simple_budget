from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
from simple_budget.helper.sql import SQL
from simple_budget.settings import START_DATE
from sqlalchemy import func
from dateutil.relativedelta import relativedelta
import calendar
import re
import collections


class BudgetType(models.Model):
    """
    budget type model
    """
    budget_type_id = models.AutoField(primary_key=True)
    budget_category = models.TextField(blank=False, null=False)
    budget_amount = models.IntegerField(unique=True, blank=False, null=False)

    @staticmethod
    def spending_by_budget_type():
        """
        get budget spend by type
        """
        simple_budget_start_date = datetime.strptime(START_DATE, '%Y-%m-%d')
        simple_budget_start_date_previous_month = \
            date(simple_budget_start_date.year,
                 simple_budget_start_date.month, 1) - relativedelta(months=1)

        end_of_this_month = date(datetime.now().year, datetime.now().month,
                                 calendar.monthrange(datetime.now().year,
                                                     datetime.now().month)[1])

        year_ago = date(datetime.now().year,
                        datetime.now().month, 1) - relativedelta(months=11)

        sql = SQL()
        spend = \
            sql.db_session.query(
                sql.budget_type.c.budget_type,
                func.SUM(sql.transaction_line.c.amount).label('amount'),
                func.DATE_TRUNC('MONTH', sql.transaction.c.transaction_date).\
                    label('year_month')).\
                join(sql.budget_category,
                     sql.budget_category.c.budget_type_id ==
                     sql.budget_type.c.budget_type_id).\
                join(sql.transaction_category,
                     sql.transaction_category.c.budget_category_id ==
                     sql.budget_category.c.budget_category_id).\
                join(sql.transaction_line,
                     sql.transaction_line.c.transaction_category_id ==
                     sql.transaction_category.c.transaction_category_id).\
                join(sql.transaction,
                     sql.transaction.c.transaction_id ==
                     sql.transaction_line.c.transaction_id). \
                filter(sql.transaction.c.transaction_date >= simple_budget_start_date_previous_month). \
                filter(sql.transaction.c.transaction_date >= year_ago). \
                filter(sql.transaction.c.transaction_date <= end_of_this_month).\
                group_by(sql.budget_type.c.budget_type,
                         func.DATE_TRUNC('MONTH', sql.transaction.c.transaction_date)).\
                order_by(func.DATE_TRUNC('MONTH', sql.transaction.c.transaction_date))

        spend = spend.all()
        spending = {}

        if spend:
            for s in spend:
                key = str(date(s.year_month.year, s.year_month.month,
                               s.year_month.day))

                if not key in spending:
                    spending[key] = {'date': s.year_month}

                spending[key][re.sub(' ', '_', s.budget_type.lower())] = abs(s.amount)

            for key, item in spending.iteritems():
                income_previous_month = \
                    str(date(item['date'].year, item['date'].month, 1) - \
                             relativedelta(months=1))

                if income_previous_month in spending.keys():
                    item['income'] = spending[income_previous_month]['income']

                item['total'] = item['income'] - item['expense'] - \
                                item['savings'] - item['debt_repayment']

            spending = collections.OrderedDict(sorted(spending.items(),
                                                      reverse=True))

            if spending.keys()[-1] < START_DATE or len(spending.keys()) > 12:
               del spending[spending.keys()[-1]]

        return spending