from __future__ import unicode_literals
from django.db import models
from django.db import connection
from datetime import datetime, date, timedelta
from simple_budget.sql import SQL
import calendar
from sqlalchemy import select, func, or_, and_


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
            select([sql.transaction_category.c.budget_category_id,
                    sql.budget_category.c.budget_category,
                    sql.budget_category.c.budget_amount,
                    func.ABS(func.SUM(sql.transaction_line.c.amount)).\
                                                        label('amount')]).\
            where(sql.transaction_line.c.transaction_category_id==
                  sql.transaction_category.c.transaction_category_id).\
            where(sql.transaction.c.transaction_id==
                  sql.transaction_line.c.transaction_id).\
            where(sql.budget_category.c.budget_category_id==
                  sql.transaction_category.c.budget_category_id).\
            where(or_(and_(sql.transaction.c.transaction_date.between(start_date,
                                                                      end_date),
                           sql.budget_category.c.expense == True).self_group(),
                      and_(sql.transaction.c.transaction_date.between(
                                         start_date_income, end_date_income),
                           sql.budget_category.c.expense ==
                                         False).self_group())).\
            group_by(sql.transaction_category.c.budget_category_id,
                     sql.budget_category.c.budget_category,
                     sql.budget_category.c.budget_amount).\
            alias('spend'))

        print str(spend)

        #print spend.count()
        """
            filter(or_(and_(sql.transaction.c.transaction_date.between(start_date,
                                                                       end_date),
                            sql.budget_category.c.expense == True),
                       and_(sql.transaction.c.transaction_date.between(
                           start_date_income, end_date_income),
                            sql.budget_category.c.expense == False))). \

        """





        """
                   or_(sql.transaction.c.transaction_date.between(
                                start_date_income, end_date_income). \
                   and_(sql.budget_category.c.expense == False)))
"""


        q = sql.db_session.query(
                select([sql.budget_category.c.budget_category_id.label('id'),
                        sql.budget_category.c.budget_category.label('category'),
                        sql.budget_category.c.expense,
                        func.COALESCE(sql.budget_category.c.budget_amount, 0).
                            label('budget_amount')]))

        cursor = connection.cursor()
        cursor.execute("SELECT    bc.budget_category_id AS id, "
                       "          bc.budget_category AS category, "
                       "          bc.expense, "
                       "          COALESCE(bc.budget_amount, 0) AS budget_amount, "
                       "          spend.amount, "
                       "          CASE "
                       "            WHEN bc.expense = TRUE "
                       "              THEN spend.difference * -1 "
                       "              ELSE spend.difference "
                       "          END AS difference, "
                       "          CASE "
                       "            WHEN spend.difference < 0 AND bc.budget_amount > 0 "
                       "              THEN @TRUNC(((spend.difference / bc.budget_amount) * 100), 2) "
                       "            ELSE 0 "
                       "          END AS overage, "
                       "          annual_spend.amount as annual_spend "
                       "FROM      budget_category bc "
                       "LEFT JOIN (SELECT    bc.budget_category_id AS id, "
                       "                     @SUM(tl.amount) AS amount, "
                       "                     bc.budget_amount - (@SUM(tl.amount)) AS difference "
                       "           FROM      transaction_line tl "
                       "           JOIN      \"transaction\" t ON (t.transaction_id = tl.transaction_id) "
                       "           JOIN      transaction_category tc ON (tc.transaction_category_id = tl.transaction_category_id) "
                       "           LEFT JOIN budget_category bc ON (bc.budget_category_id = tc.budget_category_id) "
                       "           WHERE     (   (    t.transaction_date BETWEEN '%s' AND '%s' "
                       "                          AND bc.expense = TRUE) "
                       "                      OR (    t.transaction_date BETWEEN '%s' AND '%s' "
                       "                          AND bc.expense = FALSE)) "
                       "           GROUP BY  id "
                       "           ) AS spend ON spend.id = bc.budget_category_id "
                       "LEFT JOIN (SELECT    bc.budget_category_id AS id, "
                       "                     ROUND(@(SUM(tl.amount) / 12), 2) AS amount "
                       "           FROM      transaction_line tl "
                       "           JOIN      \"transaction\" t ON (t.transaction_id = tl.transaction_id) "
                       "           JOIN      transaction_category tc ON (tc.transaction_category_id = tl.transaction_category_id) "
                       "           LEFT JOIN budget_category bc ON (bc.budget_category_id = tc.budget_category_id) "
                       "           WHERE     t.transaction_date BETWEEN '%s' AND '%s' "
                       "           GROUP BY  id "
                       "           ) AS annual_spend ON annual_spend.id = bc.budget_category_id "
                       "ORDER BY  bc.expense ASC NULLS LAST, bc.budget_amount DESC NULLS LAST" %
                       (start_date, end_date, start_date_income, end_date_income,
                        annual_start_date, annual_end_date,))

        return cursor.fetchall()

    def calculate_totals(self, transactions):
        """
        calculates total income, expense and remaining
        :param transactions:
        :return: dict
        """
        totals = {'income': {},
                  'expense': {},
                  'grand_total': {}}

        if not transactions:
            return totals
        else:
            for transaction in transactions:
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

            return totals