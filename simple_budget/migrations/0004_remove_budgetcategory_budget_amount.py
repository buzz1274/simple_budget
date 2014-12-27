# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0003_budgetcategory_budget_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budgetcategory',
            name='budget_amount',
        ),
    ]
