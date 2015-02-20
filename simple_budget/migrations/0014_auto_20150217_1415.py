# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0013_auto_20150217_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountbalance',
            name='account',
        ),
        migrations.DeleteModel(
            name='AccountBalance',
        ),
    ]
