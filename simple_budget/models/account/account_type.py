from __future__ import unicode_literals
from django.db import models


class AccountType(models.Model):
    """
    account type model
    """
    account_type_id = models.AutoField(primary_key=True)
    account_type = models.TextField(blank=False, null=False)
    ordering = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        db_table = 'account_type'