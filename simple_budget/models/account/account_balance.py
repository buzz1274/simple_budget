from __future__ import unicode_literals
from django.db import models
from account import Account


class AccountBalance(models.Model):
    """
    account model
    """
    account_balance_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, blank=False, null=False)
    account_balance = \
        models.DecimalField(max_digits=7, decimal_places=2, blank=True,
                            null=True)
    account_balance_date = models.DateField(null=False, blank=False)

    class Meta:
        db_table = 'account_balance'