from __future__ import unicode_literals
from django.db import models
from simple_budget.models.transaction.transaction import Transaction
from simple_budget.models.transaction.transaction_category import TransactionCategory


class TransactionLine(models.Model):
    """
    transaction line model
    """
    transaction_line_id = models.IntegerField(primary_key=True)
    transaction = models.ForeignKey(Transaction, blank=True, null=True)
    transaction_category = \
        models.ForeignKey(TransactionCategory, blank=True, null=True)
    amount = \
        models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'transaction_line'
