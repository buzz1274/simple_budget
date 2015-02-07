# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0004_remove_budgetcategory_budget_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('account_type_id', models.AutoField(serialize=False, primary_key=True)),
                ('account_type', models.TextField()),
                ('ordering', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'account_type',
            },
            bases=(models.Model,),
        ),
    ]
