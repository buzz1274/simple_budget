# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0014_auto_20150217_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_hidden',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
