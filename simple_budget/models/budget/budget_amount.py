from __future__ import unicode_literals
from django.db import models
from simple_budget.models.budget.budget_category import BudgetCategory


class BudgetAmount(models.Model):
    """
    budget category model
    """
    budget_amount_id = models.AutoField(primary_key=True)
    budget = models.ForeignKey('Budget', blank=False, null=True)
    budget_category = models.ForeignKey(BudgetCategory, blank=False, null=True)
    budget_amount = models.DecimalField(max_digits=7, decimal_places=2,
                                        blank=True, null=True)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'budget_amount'