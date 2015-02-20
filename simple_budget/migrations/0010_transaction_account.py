# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0009_auto_20150207_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(blank=True, to='simple_budget.Account', null=True),
            preserve_default=True,
        ),
    ]
