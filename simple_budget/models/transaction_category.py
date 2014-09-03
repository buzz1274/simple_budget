from __future__ import unicode_literals
from django.db import models

class TransactionCategory(models.Model):
    """
    transaction category model
    """
    transaction_category_id = models.IntegerField(primary_key=True)
    transaction_category_parent = models.ForeignKey('self', blank=True,
                                                    null=True)
    budget_category_id = models.IntegerField(blank=True, null=True)
    transaction_category = models.TextField(blank=True)

    class Meta:
        db_table = 'transaction_category'
