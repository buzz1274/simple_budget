# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0012_auto_20150217_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_starting_balance',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='accountbalance',
            name='account_balance',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=2),
            preserve_default=False,
        ),
    ]
