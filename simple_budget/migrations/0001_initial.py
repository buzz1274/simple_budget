# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('budget_id', models.AutoField(serialize=False, primary_key=True)),
                ('budget_name', models.TextField()),
                ('budget_description', models.TextField()),
                ('budget_master', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'budget',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BudgetCategory',
            fields=[
                ('budget_category_id', models.AutoField(serialize=False, primary_key=True)),
                ('budget_category', models.TextField(blank=True)),
                ('budget_amount', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
            ],
            options={
                'db_table': 'budget_category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BudgetType',
            fields=[
                ('budget_type_id', models.AutoField(serialize=False, primary_key=True)),
                ('budget_type', models.TextField()),
                ('ordering', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'budget_type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QIFParser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parse_status', models.TextField(null=True, blank=True)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'qif_parser',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(serialize=False, primary_key=True)),
                ('transaction_date', models.DateField()),
            ],
            options={
                'db_table': 'transaction',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionCategory',
            fields=[
                ('transaction_category_id', models.AutoField(serialize=False, primary_key=True)),
                ('transaction_category', models.TextField(blank=True)),
                ('budget_category', models.ForeignKey(blank=True, to='simple_budget.BudgetCategory', null=True)),
                ('transaction_category_parent', models.ForeignKey(blank=True, to='simple_budget.TransactionCategory', null=True)),
            ],
            options={
                'db_table': 'transaction_category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionLine',
            fields=[
                ('transaction_line_id', models.AutoField(serialize=False, primary_key=True)),
                ('amount', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('transaction', models.ForeignKey(blank=True, to='simple_budget.Transaction', null=True)),
                ('transaction_category', models.ForeignKey(blank=True, to='simple_budget.TransactionCategory', null=True)),
            ],
            options={
                'db_table': 'transaction_line',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='budgetcategory',
            name='budget_type',
            field=models.ForeignKey(blank=True, to='simple_budget.BudgetType', null=True),
            preserve_default=True,
        ),
    ]
