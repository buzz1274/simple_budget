from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
from simple_budget.helper.sql import SQL
from simple_budget.settings import START_DATE
from sqlalchemy import func
from dateutil.relativedelta import relativedelta
import decimal
import calendar
import re
import collections


class BudgetType(models.Model):
    """
    budget type model
    """
    budget_type_id = models.AutoField(primary_key=True)
    budget_type = models.TextField(blank=False, null=False)
    ordering = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        db_table = 'budget_type'

    def __unicode__(self):
        return self.budget_type

    @staticmethod
    def spending_by_budget_type(year=None):
        """
        retrieves spending by budget type for the last 12 months
        """
        simple_budget_start_date = datetime.strptime(START_DATE, '%Y-%m-%d')
        end_of_this_month = date(datetime.now().year, datetime.now().month,
                                 calendar.monthrange(datetime.now().year,
                                                     datetime.now().month)[1])

        if not year:
            date_trunc = 'YEAR'
        else:
            date_trunc = 'MONTH'
            simple_budget_start_date_previous_month = \
                date(simple_budget_start_date.year,
                     simple_budget_start_date.month, 1) - relativedelta(months=1)

            start_of_year = date(year, 1, 1)
            end_of_year = date(year, 12, 31)

        sql = SQL()
        spend = \
            sql.db_session.query(
                sql.budget_type.c.budget_type,
                func.SUM(sql.transaction_line.c.amount).label('amount'),
                func.DATE_TRUNC(date_trunc, sql.transaction.c.transaction_date).\
                    label('date')).\
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
                     sql.transaction_line.c.transaction_id).\
                filter(sql.transaction.c.transaction_date >= simple_budget_start_date). \
                filter(sql.transaction.c.transaction_date <= end_of_this_month)

        if year:
            spend = \
                spend.filter(sql.transaction.c.transaction_date >= simple_budget_start_date_previous_month). \
                      filter(sql.transaction.c.transaction_date >= start_of_year). \
                      filter(sql.transaction.c.transaction_date <= end_of_year)

        spend = \
            spend.group_by(sql.budget_type.c.budget_type,
                           func.DATE_TRUNC(date_trunc, sql.transaction.c.transaction_date)). \
                  order_by(func.DATE_TRUNC(date_trunc, sql.transaction.c.transaction_date))

        spend = spend.all()
        spending = {}
        average_spending = {}
        total_spending = {'income': 0, 'expense': 0,
                          'savings': 0, 'debt_repayment': 0,
                          'total': 0}

        if not spend:
            return [False, False, False]
        else:
            for s in spend:
                if not year:
                    key = s.date.year
                else:
                    key = str(date(s.date.year, s.date.month,
                                   s.date.day))

                if not key in spending:
                    spending[key] = {'date': s.date}

                category_key = re.sub(' ', '_', s.budget_type.lower())

                if s.budget_type.lower() != 'income':
                    spending[key][category_key] = s.amount * -1
                else:
                    spending[key][category_key] = abs(s.amount)

                if not year:
                    if date.today().year == s.date.year:
                        average_divisor = date.today().month
                    else:
                        average_divisor = 12

                    spending[key][category_key+'_average'] = \
                        spending[key][category_key] / average_divisor

            for key, item in spending.iteritems():
                item['debt_repayment'] = \
                    item['income'] - \
                    item['expense'] - \
                    item['savings']

                if not year:
                    if date.today().year == key:
                        average_divisor = date.today().month
                    else:
                        average_divisor = 12

                    item['debt_repayment_average'] = item['debt_repayment'] / average_divisor

            spending = collections.OrderedDict(sorted(spending.items(),
                                                      reverse=True))

            for key, item in spending.iteritems():
                for item_key, value in item.iteritems():
                    if item_key != 'date' and not item_key in total_spending:
                        total_spending[item_key] = value
                    elif item_key != 'date':
                        total_spending[item_key] += value

            for key, value in total_spending.iteritems():
                average_spending[key] = decimal.Decimal(value) / \
                                        decimal.Decimal(len(spending))

            return [total_spending, average_spending, spending]