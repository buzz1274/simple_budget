# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0007_auto_20150207_0920'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='account',
            table='account',
        ),
        migrations.AlterModelTable(
            name='accountbalance',
            table='account_balance',
        ),
    ]
