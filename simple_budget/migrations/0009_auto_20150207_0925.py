# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0008_auto_20150207_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_notes',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
