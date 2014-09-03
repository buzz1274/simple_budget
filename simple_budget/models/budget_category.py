from __future__ import unicode_literals
from django.db import models
from django.db import connection

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
        cursor = connection.cursor()
        cursor.execute("SELECT    bc.budget_category_id AS id, "
                       "          bc.budget_category AS category, "
                       "          bc.expense, bc.budget_amount, spend.amount, "
                       "          spend.remaining "
                       "FROM      budget_category bc "
                       "LEFT JOIN (SELECT    bc.budget_category_id AS id, "
                       "                     @SUM(tl.amount) AS amount, "
                       "                     bc.budget_amount - @SUM(tl.amount) AS remaining "
                       "           FROM      transaction_line tl "
                       "           JOIN      \"transaction\" t ON (t.transaction_id = tl.transaction_id) "
                       "           JOIN      transaction_category tc ON (tc.transaction_category_id = tl.transaction_category_id) "
                       "           LEFT JOIN budget_category bc ON (bc.budget_category_id = tc.budget_category_id) "
                       "           WHERE     t.transaction_date BETWEEN '%s' AND '%s' "
                       "           GROUP BY  id "
                       "           ) AS spend ON spend.id = bc.budget_category_id "
                       "ORDER BY  bc.expense ASC NULLS LAST, bc.budget_amount DESC NULLS LAST" %
                       (start_date, end_date,))

        return cursor.fetchall()