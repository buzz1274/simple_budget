# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0010_transaction_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetcategory',
            name='budget_type',
            field=models.ForeignKey(to='simple_budget.BudgetType', blank=True),
            preserve_default=True,
        ),
    ]
