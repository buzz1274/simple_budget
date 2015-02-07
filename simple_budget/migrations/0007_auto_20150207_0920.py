# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0006_delete_accounttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.AutoField(serialize=False, primary_key=True)),
                ('account_name', models.TextField(blank=True)),
                ('account_notes', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AccountBalance',
            fields=[
                ('account_balance_id', models.AutoField(serialize=False, primary_key=True)),
                ('account_balance', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('account_balance_date', models.DateField()),
                ('account', models.ForeignKey(to='simple_budget.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.AddField(
            model_name='account',
            name='account_type',
            field=models.ForeignKey(blank=True, to='simple_budget.AccountType', null=True),
            preserve_default=True,
        ),
    ]
