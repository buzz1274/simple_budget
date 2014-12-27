# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_budget', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetAmount',
            fields=[
                ('budget_amount_id', models.AutoField(serialize=False, primary_key=True)),
                ('budget_amount', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('budget', models.ForeignKey(to='simple_budget.Budget', null=True)),
                ('budget_category', models.ForeignKey(to='simple_budget.BudgetCategory', null=True)),
            ],
            options={
                'db_table': 'budget_amount',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='budgetcategory',
            name='budget_amount',
        ),
    ]

