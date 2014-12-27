# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0002_auto_20141212_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetcategory',
            name='budget_amount',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]

