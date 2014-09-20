from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date, timedelta
from simple_budget.sql import SQL
from sqlalchemy import func, or_, and_, case
import calendar


class BudgetCategory(models.Model):
    """
    budget category model
    """
    budget_category_id = models.IntegerField(primary_key=True)
    budget_category = models.TextField(blank=True)
    budget_amount = models.DecimalField(max_digits=7, decimal_places=2,
                                        blank=True, null=True)

    class Meta:
        db_table = 'budget_category'

    def budget_transactions(self, start_date=None, end_date=None):
        """
        retrieves spending by budget category between the specified dates
        :return: dict
        """
        if not start_date or not end_date:
            today = date(datetime.now().year, datetime.now().month,
                         datetime.now().day)
            start_date = date(datetime.now().year, datetime.now().month, 1)
            end_date = date(datetime.now().year, datetime.now().month,
                            calendar.monthrange(datetime.now().year,
                                                datetime.now().month)[1])

            if end_date > today:
                end_date = today

        end_date_income = start_date - timedelta(1)
        start_date_income = date(end_date_income.year, end_date_income.month, 1)
        annual_start_date = date(today.year - 1, today.month, 1)
        annual_end_date = date(today.year, today.month - 1,
                               calendar.monthrange(today.year,
                                                   today.month - 1)[1])

        sql = SQL()
        spend = sql.db_session.query(
                    sql.transaction_category.c.budget_category_id.label('id'),
                    func.ABS(func.SUM(sql.transaction_line.c.amount)).\
                        label('amount'),
                    (sql.budget_category.c.budget_amount -
                     func.ABS(func.SUM(sql.transaction_line.c.amount))).\
                        label('difference')).\
            filter(sql.transaction_line.c.transaction_category_id==
                   sql.transaction_category.c.transaction_category_id).\
            filter(sql.transaction.c.transaction_id==
                   sql.transaction_line.c.transaction_id). \
            filter(sql.budget_category.c.budget_category_id==
                   sql.transaction_category.c.budget_category_id). \
            filter(sql.budget_category.c.budget_type_id==
                   sql.budget_type.c.budget_type_id). \
            filter(or_(and_(sql.transaction.c.transaction_date.between(start_date,
                                                                      end_date),
                            sql.budget_type.c.budget_type != 'Income').self_group(),
                       and_(sql.transaction.c.transaction_date.between(
                            start_date_income, end_date_income),
                            sql.budget_type.c.budget_type == 'Income').self_group())).\
            group_by(sql.transaction_category.c.budget_category_id,
                     sql.budget_category.c.budget_category,
                     sql.budget_category.c.budget_amount).subquery()

        annual_spend = sql.db_session.query(
                    sql.transaction_category.c.budget_category_id.label('id'),
                    func.ROUND(
                        func.ABS(
                            func.SUM(sql.transaction_line.c.amount) / 12), 2).\
                                label('amount')).\
            filter(sql.transaction_line.c.transaction_category_id==
                   sql.transaction_category.c.transaction_category_id). \
            filter(sql.transaction.c.transaction_id==
                   sql.transaction_line.c.transaction_id).\
            filter(sql.budget_category.c.budget_category_id==
                   sql.transaction_category.c.budget_category_id).\
            filter(sql.transaction.c.transaction_date.between(annual_start_date,
                                                              annual_end_date)).\
            group_by(sql.transaction_category.c.budget_category_id,
                     sql.budget_category.c.budget_category,
                     sql.budget_category.c.budget_amount).subquery()

        budget = \
            sql.db_session.query(sql.budget_category.c.budget_category_id,
                                 sql.budget_category.c.budget_category,
                                 sql.budget_type.c.ordering,
                                 sql.budget_type.c.budget_type,
                                 spend.c.difference.label('difference'),
                                 func.COALESCE(sql.budget_category.c.budget_amount,
                                               0).label('budget_amount'),
                                 spend.c.amount.label('actual_spend'),
                                 case([(and_(spend.c.difference < 0,
                                             sql.budget_category.c.budget_amount > 0),
                                       func.TRUNC(func.ABS((spend.c.difference /
                                                            sql.budget_category.c.budget_amount)
                                                  * 100),2)),
                                      ], else_=0).label('overage'),
                                 annual_spend.c.amount.label('average_annual_spend')).\
                        join(sql.budget_type,
                             sql.budget_type.c.budget_type_id ==
                             sql.budget_category.c.budget_type_id).\
                        outerjoin(spend,
                                  and_(spend.c.id==
                                       sql.budget_category.c.budget_category_id)).\
                        outerjoin(annual_spend,
                                  and_(annual_spend.c.id==
                                       sql.budget_category.c.budget_category_id)).\
                        order_by(sql.budget_type.c.ordering.asc()).\
                        order_by(sql.budget_category.c.budget_amount.desc().nullslast())

        return budget.all()

    def calculate_totals(self, transactions):
        """
        calculates total income, expense and remaining
        :param transactions:
        :return: dict
        """
        if not transactions:
            return False
        else:
            totals = {}
            sorted_totals = []

            for transaction in transactions:
                if transaction.budget_type not in totals:
                    totals[transaction.budget_type] = \
                        {'actual': 0, 'budget': 0, 'average_annual': 0,
                         'budget_type': transaction.budget_type,
                         'ordering': transaction.ordering}

                if transaction.actual_spend:
                    totals[transaction.budget_type]['actual'] += \
                        transaction.actual_spend

                if transaction.budget_amount:
                    totals[transaction.budget_type]['budget'] += \
                        transaction.budget_amount

                if transaction.average_annual_spend:
                    totals[transaction.budget_type]['average_annual'] += \
                        transaction.average_annual_spend

            for key, total in totals.iteritems():
                total['difference'] = total['budget'] - total['actual']
                total['overage'] = 1234
                sorted_totals.append(total)

            sorted_totals = sorted(sorted_totals, key=lambda k: k['ordering'])

            return sorted_totals
            """
            if transaction[1] == 'Income' and not transaction[2]:
                totals['income'] = {'actual': transaction[4],
                                    'budget': transaction[3],
                                    'average': transaction[7],
                                    'difference': abs(transaction[5])}

                print transaction

                if (totals['income']['difference'] and
                    totals['income']['actual']):
                    totals['income']['overage'] = \
                        str(round(abs(((totals['income']['difference'] /
                                        totals['income']['actual']) * 100)), 2))

            elif transaction[2]:
                if transaction[4]:
                    if (not totals['expense'] or
                        'actual' not in totals['expense']):
                        totals['expense']['actual'] = transaction[4]
                    else:
                        totals['expense']['actual'] += transaction[4]
                if transaction[3]:
                    if (not totals['expense'] or
                        'budget' not in totals['expense']):
                        totals['expense']['budget'] = transaction[3]
                    else:
                        totals['expense']['budget'] += transaction[3]

                if transaction[7]:
                    if (not totals['expense'] or
                        'average' not in totals['expense']):
                        totals['expense']['average'] = transaction[7]
                    else:
                        totals['expense']['average'] += transaction[7]

        if ('actual' in totals['expense'] and
            'actual' in totals['income'] and
            'budget' in totals['expense']):

            totals['expense']['difference'] = \
                totals['expense']['budget'] - totals['expense']['actual']

            totals['grand_total']['actual'] = \
                totals['income']['actual'] - totals['expense']['actual']

            totals['grand_total']['budget'] = \
                totals['income']['budget'] - totals['expense']['budget']

            if totals['expense']['difference'] < 0:
                totals['expense']['overage'] = \
                    abs(round(((totals['expense']['difference'] /
                                totals['expense']['actual']) * 100), 2))

        if 'average' in totals['expense'] and 'average' in totals['income']:
            totals['grand_total']['average'] = \
                totals['income']['average'] - totals['expense']['average']
        """