# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0016_account_account_opening_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='account_opening_date',
        ),
        migrations.RemoveField(
            model_name='account',
            name='account_starting_balance',
        ),
    ]
