# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0011_auto_20150217_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetcategory',
            name='budget_type',
            field=models.ForeignKey(blank=True, to='simple_budget.BudgetType', null=True),
            preserve_default=True,
        ),
    ]
