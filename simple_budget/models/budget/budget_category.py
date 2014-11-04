from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date, timedelta
from simple_budget.helper.sql import SQL
from sqlalchemy import func, or_, and_, case
from dateutil.relativedelta import relativedelta
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

    def spending_by_budget_category(self, start_date=None, end_date=None):
        """
        retrieves spending by budget category between the specified dates
        :return: dict
        """
        if not start_date or not end_date:
            start_date = date(datetime.now().year, datetime.now().month, 1)
            end_date = date(datetime.now().year, datetime.now().month,
                            calendar.monthrange(datetime.now().year,
                                                datetime.now().month)[1])

        today = date(datetime.now().year, datetime.now().month,
                     datetime.now().day)
        end_date_income = start_date - timedelta(1)
        start_date_income = date(end_date_income.year, end_date_income.month, 1)


        annual_start_date = date(today.year, start_date.month, 1) - \
                            relativedelta(years=1)
        annual_end_date = date(start_date.year, start_date.month, 1) - \
                          relativedelta(months=1)
        annual_end_date = date(annual_end_date.year, annual_end_date.month,
                               calendar.monthrange(annual_end_date.year,
                                                   annual_end_date.month)[1])

        sql = SQL()
        spend = sql.db_session.query(
                    sql.transaction_category.c.budget_category_id.label('id'),
                    func.SUM(sql.transaction_line.c.amount).\
                        label('amount'),
                    case([(sql.budget_type.c.budget_type != 'Expense',
                           func.ABS(func.SUM(sql.transaction_line.c.amount)) -
                           sql.budget_category.c.budget_amount),
                          (sql.budget_type.c.budget_type == 'Expense',
                           sql.budget_category.c.budget_amount -
                           func.ABS(func.SUM(sql.transaction_line.c.amount))),
                          ], else_=0).label('difference')).\
            filter(sql.transaction_line.c.transaction_category_id==
                   sql.transaction_category.c.transaction_category_id).\
            filter(sql.transaction.c.transaction_id==
                   sql.transaction_line.c.transaction_id). \
            filter(sql.budget_category.c.budget_category_id==
                   sql.transaction_category.c.budget_category_id).\
            filter(sql.budget_category.c.budget_type_id==
                   sql.budget_type.c.budget_type_id).\
            filter(or_(and_(sql.transaction.c.transaction_date.between(start_date,
                                                                      end_date),
                            sql.budget_type.c.budget_type != 'Income').self_group(),
                       and_(sql.transaction.c.transaction_date.between(
                            start_date_income, end_date_income),
                            sql.budget_type.c.budget_type == 'Income').self_group())).\
            group_by(sql.transaction_category.c.budget_category_id,
                     sql.budget_category.c.budget_category,
                     sql.budget_category.c.budget_amount,
                     sql.budget_type.c.budget_type).subquery()

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
                                 case([(and_(spend.c.difference != 0,
                                             sql.budget_category.c.budget_amount > 0),
                                       func.ROUND(func.ABS((spend.c.difference /
                                                            sql.budget_category.c.budget_amount)
                                                  * 100),2)),
                                      ], else_=0).label('difference_percent'),
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
                        order_by(sql.budget_category.c.budget_amount.desc().nullslast()).\
                        order_by(sql.budget_category.c.budget_category.asc())

        transactions = budget.all()
        sorted_totals, grand_total = self.calculate_totals(transactions)

        return [transactions, sorted_totals, grand_total]

    @staticmethod
    def calculate_totals(transactions):
        """
        calculates total income, expense and remaining
        :param transactions:
        :return: dict
        """
        if not transactions:
            return [False, False]
        else:
            totals = {}
            grand_total = {'budget': 0, 'actual': 0, 'average_annual': 0}
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

                    transaction.actual_spend = abs(transaction.actual_spend)

                if transaction.budget_amount:
                    totals[transaction.budget_type]['budget'] += \
                        transaction.budget_amount

                if transaction.average_annual_spend:
                    totals[transaction.budget_type]['average_annual'] += \
                        transaction.average_annual_spend

            for key, total in totals.iteritems():
                total['actual'] = abs(total['actual'])

                if total['budget_type'] == 'Expense':
                    total['difference'] = total['budget'] - total['actual']
                else:
                    total['difference'] = total['actual'] - total['budget']

                if total['difference'] != 0:
                    total['difference_percent'] = \
                        abs(round(((total['difference'] /
                                    total['budget']) * 100), 2))

                sorted_totals.append(total)

                if key == 'Income':
                    grand_total['budget'] += total['budget']
                    grand_total['actual'] += total['actual']
                    grand_total['average_annual'] += total['average_annual']
                else:
                    grand_total['budget'] -= total['budget']
                    grand_total['actual'] -= total['actual']
                    grand_total['average_annual'] -= total['average_annual']

            grand_total['difference'] = grand_total['actual'] - \
                                        grand_total['budget']

            if grand_total['difference'] != 0:
                grand_total['difference_percent'] =\
                    abs(round(((float(grand_total['difference']) /
                                float(grand_total['budget'])) * 100), 2))

            sorted_totals = sorted(sorted_totals, key=lambda k: k['ordering'])

            return [sorted_totals, grand_total]