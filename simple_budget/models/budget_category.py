from __future__ import unicode_literals
from django.db import models
from django.db import connection
from datetime import date
import datetime

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

    def budget_transactions(self, start_date, end_date):
        """
        retrieves spending by budget category between the specified dates
        :return: dict
        """
        end_date_income = start_date - datetime.timedelta(1)
        start_date_income = date(end_date_income.year, end_date_income.month, 1)

        cursor = connection.cursor()
        cursor.execute("SELECT    bc.budget_category_id AS id, "
                       "          bc.budget_category AS category, "
                       "          bc.expense, COALESCE(bc.budget_amount, 0) AS budget_amount, "
                       "          spend.amount, spend.remaining, "
                       "          CASE "
                       "            WHEN bc.expense = TRUE AND spend.remaining < 0 AND bc.budget_amount > 0 "
                       "              THEN @ROUND(((spend.remaining / bc.budget_amount) * 100), 2) "
                       "            ELSE 0 "
                       "          END AS overage "
                       "FROM      budget_category bc "
                       "LEFT JOIN (SELECT    bc.budget_category_id AS id, "
                       "                     @SUM(tl.amount) AS amount, "
                       "                     bc.budget_amount - @SUM(tl.amount) AS remaining "
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
                       "ORDER BY  bc.expense ASC NULLS LAST, bc.budget_amount DESC NULLS LAST" %
                       (start_date, end_date, start_date_income, end_date_income,))

        return cursor.fetchall()

    def calculate_totals(self, transactions):
        """
        calculates total income, expense and remaining
        :param transactions:
        :return: float
        """
        totals = {'income': {},
                  'expense': {}}

        if not transactions:
            return totals
        else:
            for transaction in transactions:
                if transaction[1] == 'Income' and not transaction[2]:
                    totals['income'] = {'actual': transaction[4],
                                        'budget': transaction[3],
                                        'difference': abs(transaction[4] - transaction[3])}
                    if transaction[3]:
                        totals['income']['overage'] = (totals['income']['overage'] / transaction[3]) * 100
                elif transaction[2]:
                    if transaction[4]:
                        if not totals['expense'] or 'actual' not in totals['expense']:
                            totals['expense']['actual'] = transaction[4]
                        else:
                            totals['expense']['actual'] += transaction[4]
                    if transaction[3]:
                        if not totals['expense'] or 'budget' not in totals['expense']:
                            totals['expense']['budget'] = transaction[3]
                        else:
                            totals['expense']['budget'] += transaction[3]

            totals['expense']['difference'] = totals['expense']['budget'] - \
                                              totals['expense']['actual']

            if totals['expense']['difference'] < 0:
                totals['expense']['overage'] = abs(round(((totals['expense']['difference'] /
                                                           totals['expense']['actual']) * 100), 2))

            return totals