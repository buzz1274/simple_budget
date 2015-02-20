# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0015_account_account_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_opening_date',
            field=models.DateField(default=datetime.datetime(2015, 2, 19, 8, 41, 44, 534230, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
