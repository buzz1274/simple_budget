from __future__ import unicode_literals
from django.db import models, transaction, DatabaseError
from django.db.models import Q
from simple_budget.models.budget.budget_amount import BudgetAmount
from simple_budget.models.budget.budget_category import BudgetCategory
from simple_budget.helper.sql import SQL
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from sqlalchemy import func, or_, and_, case, Table, MetaData
from decimal import Decimal
import re
import calendar


class Budget(models.Model):
    """
    budget category model
    """
    budget_id = models.AutoField(primary_key=True)
    budget_name = models.TextField(blank=False, null=False)
    budget_description = models.TextField(blank=False, null=False)
    budget_master = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        db_table = 'budget'

    def get_budget(self, start_date, end_date, budget_id=None):
        """
        retrieves spending by budget category between the specified dates
        :return: dict
        """
        if not start_date or not end_date:
            return [None, None, None]

        if not budget_id:
            budget = Budget.objects.filter(budget_master=True)
            if not budget:
                budget_id = None
            else:
                budget_id = budget[0].budget_id

        end_date_income = start_date - timedelta(1)
        start_date_income = date(end_date_income.year, end_date_income.month, 1)


        annual_start_date = date(start_date.year, start_date.month, 1) - \
                            relativedelta(years=1)
        annual_end_date = date(start_date.year, start_date.month, 1) - \
                          relativedelta(months=1)
        annual_end_date = date(annual_end_date.year, annual_end_date.month,
                               calendar.monthrange(annual_end_date.year,
                                                   annual_end_date.month)[1])

        next_month_start_date = date(start_date.year, start_date.month, 1) + \
                                relativedelta(months=1)
        next_month_end_date = \
            date(next_month_start_date.year,
                 next_month_start_date.month,
                 calendar.monthrange(next_month_start_date.year,
                                     next_month_start_date.month)[1])

        sql = SQL()
        budget_amount_future =\
            Table('budget_amount', MetaData(), autoload=True,
                  autoload_with=sql.db).alias('budget_amount_future')

        spend = sql.db_session.query(
            sql.budget_category.c.budget_category_id.label('id'),
            sql.budget_amount.c.budget_amount,
            budget_amount_future.c.budget_amount.label('budget_amount_future'),
            func.SUM(sql.transaction_line.c.amount).label('amount'),
            case([(sql.budget_type.c.budget_type != 'Expense',
                   func.ABS(func.SUM(sql.transaction_line.c.amount)) -
                            sql.budget_amount.c.budget_amount
                   ),
                  (sql.budget_type.c.budget_type == 'Expense',
                   case([(func.SUM(sql.transaction_line.c.amount) < 0,
                          sql.budget_amount.c.budget_amount -
                          func.ABS(func.SUM(sql.transaction_line.c.amount)))],
                        else_=sql.budget_amount.c.budget_amount +
                              func.ABS(func.SUM(sql.transaction_line.c.amount))
                   )),
                  ]).label('difference')).\
            join(sql.budget_type,
                 sql.budget_type.c.budget_type_id==sql.budget_category.c.budget_type_id). \
            outerjoin(sql.transaction_category,
                      sql.transaction_category.c.budget_category_id==
                      sql.budget_category.c.budget_category_id). \
            outerjoin(sql.budget,
                      and_(sql.budget.c.budget_id == budget_id)). \
            outerjoin(sql.budget_amount,
                      and_(sql.budget.c.budget_id==sql.budget_amount.c.budget_id,
                           sql.budget_amount.c.budget_category_id==
                           sql.budget_category.c.budget_category_id,
                           sql.budget_amount.c.start_date <= start_date,
                           or_(sql.budget_amount.c.end_date == None,
                               sql.budget_amount.c.end_date >= end_date))). \
            outerjoin(budget_amount_future,
                      and_(sql.budget.c.budget_id==budget_amount_future.c.budget_id,
                           budget_amount_future.c.budget_category_id==
                           sql.budget_category.c.budget_category_id,
                           budget_amount_future.c.start_date <= next_month_start_date,
                           or_(budget_amount_future.c.end_date == None,
                               budget_amount_future.c.end_date >= next_month_end_date))). \
            outerjoin(sql.transaction,
                      or_(and_(sql.transaction.c.transaction_date.between(start_date,
                                                                          end_date),
                               sql.budget_type.c.budget_type != 'Income').self_group(),
                          and_(sql.transaction.c.transaction_date.between(
                              start_date_income, end_date_income),
                               sql.budget_type.c.budget_type == 'Income').self_group())). \
            outerjoin(sql.transaction_line,
                      and_(sql.transaction_line.c.transaction_id==
                           sql.transaction.c.transaction_id,
                           sql.transaction_category.c.transaction_category_id ==
                           sql.transaction_line.c.transaction_category_id)). \
            group_by(sql.budget_category.c.budget_category_id,
                     sql.budget_category.c.budget_category,
                     sql.budget_amount.c.budget_amount,
                     budget_amount_future.c.budget_amount,
                     sql.budget_type.c.budget_type).subquery()

        annual_spend = sql.db_session.query(
            sql.transaction_category.c.budget_category_id.label('id'),
            func.ROUND(
                func.ABS(
                    func.SUM(sql.transaction_line.c.amount) / 12), 2). \
            label('amount')). \
            filter(sql.transaction_line.c.transaction_category_id==
                   sql.transaction_category.c.transaction_category_id). \
            filter(sql.transaction.c.transaction_id==
                   sql.transaction_line.c.transaction_id). \
            filter(sql.budget_category.c.budget_category_id==
                   sql.transaction_category.c.budget_category_id). \
            filter(sql.transaction.c.transaction_date.between(annual_start_date,
                                                              annual_end_date)). \
            group_by(sql.transaction_category.c.budget_category_id,
                     sql.budget_category.c.budget_category).subquery()

        budget = \
            sql.db_session.query(sql.budget_category.c.budget_category_id,
                                 sql.budget_category.c.budget_category,
                                 sql.budget_type.c.ordering,
                                 sql.budget_type.c.budget_type_id,
                                 sql.budget_type.c.budget_type,
                                 spend.c.budget_amount,
                                 spend.c.budget_amount_future,
                                 spend.c.difference.label('difference'),
                                 func.COALESCE(spend.c.budget_amount,
                                               0).label('budget_amount'),
                                 spend.c.amount.label('actual_spend'),
                                 case([(and_(spend.c.difference != 0,
                                             spend.c.budget_amount > 0),
                                        func.ROUND(func.ABS((spend.c.difference /
                                                             spend.c.budget_amount)
                                                            * 100),2)),
                                       ], else_=0).label('difference_percent'),
                                 annual_spend.c.amount.label('average_annual_spend')). \
                join(sql.budget_type,
                     sql.budget_type.c.budget_type_id ==
                     sql.budget_category.c.budget_type_id). \
                outerjoin(spend,
                          and_(spend.c.id==
                               sql.budget_category.c.budget_category_id)). \
                outerjoin(annual_spend,
                          and_(annual_spend.c.id==
                               sql.budget_category.c.budget_category_id)). \
                order_by(sql.budget_type.c.ordering.asc()). \
                order_by(sql.budget_category.c.budget_category.asc())

        transactions = budget.all()

        transactions, sorted_totals, grand_total = \
            self.calculate_totals(transactions)

        return [transactions, sorted_totals, grand_total]

    def add_edit_budget(self, action, data):
        """
        :param action:
        :param data:
        :return: boolean
        """
        if 'budget_master' in data.keys():
            budget_master = True
        else:
            budget_master = False

        try:
            with transaction.atomic():
                if action == 'add':
                    return self.add_budget(data, budget_master)
                elif action == 'edit':
                    return self.edit_budget(data, budget_master)
                else:
                    return False
        except DatabaseError:
            return False

    def delete_budget(self):
        """
        delete the current budget and associated budget amounts
        :return: boolean
        """
        try:
            with transaction.atomic():
                BudgetAmount.objects.filter(budget_id=self.budget_id).delete()
                Budget.objects.filter(budget_id=self.budget_id).delete()

                return True

        except DatabaseError:
            return False

    @staticmethod
    def calculate_totals(transactions):
        """
        calculates total income, expense and remaining
        :param transactions:
        :return: dict
        """
        if not transactions:
            return [False, False]
        else:
            totals = {}
            grand_total = {'budget': 0, 'actual': 0, 'average_annual': 0,
                           'budget_future': 0}
            sorted_totals = []

            for transaction in transactions:
                if transaction.budget_type not in totals:
                    totals[transaction.budget_type] = \
                        {'actual': 0, 'budget': 0, 'average_annual': 0,
                         'budget_future':0,
                         'budget_type': transaction.budget_type,
                         'budget_type_id': transaction.budget_type_id,
                         'ordering': transaction.ordering}

                if transaction.actual_spend:
                    totals[transaction.budget_type]['actual'] += \
                        transaction.actual_spend

                    if transaction.budget_type == 'Expense':
                        transaction.actual_spend *= -1
                    else:
                        transaction.actual_spend = abs(transaction.actual_spend)

                if transaction.budget_amount:
                    totals[transaction.budget_type]['budget'] += \
                        transaction.budget_amount

                if transaction.budget_amount_future:
                    totals[transaction.budget_type]['budget_future'] += \
                        transaction.budget_amount_future

                if transaction.average_annual_spend:
                    totals[transaction.budget_type]['average_annual'] += \
                        transaction.average_annual_spend

            for key, total in totals.iteritems():
                total['actual'] = abs(total['actual'])

                if total['budget_type'] == 'Expense':
                    total['difference'] = total['budget'] - total['actual']
                else:
                    total['difference'] = total['actual'] - total['budget']

                if total['difference'] != 0 and total['budget'] != 0:
                    total['difference_percent'] = \
                        abs(round(((total['difference'] /
                                    total['budget']) * 100), 2))

                sorted_totals.append(total)

                if key == 'Income':
                    grand_total['budget'] += total['budget']
                    grand_total['budget_future'] += total['budget_future']
                    grand_total['actual'] += total['actual']
                    grand_total['average_annual'] += total['average_annual']
                else:
                    grand_total['budget'] -= total['budget']
                    grand_total['budget_future'] -= total['budget_future']
                    grand_total['actual'] -= total['actual']
                    grand_total['average_annual'] -= total['average_annual']

            grand_total['difference'] = grand_total['actual'] - \
                                        grand_total['budget']

            if grand_total['difference'] != 0 and grand_total['budget'] != 0:
                grand_total['difference_percent'] = \
                    abs(round(((float(grand_total['difference']) /
                                float(grand_total['budget'])) * 100), 2))

            sorted_totals = sorted(sorted_totals, key=lambda k: k['ordering'])

            return [transactions, sorted_totals, grand_total]

    @staticmethod
    def add_budget(data, budget_master):
        """
        add a new budget
        """
        budget = Budget(budget_name=data['budget_name'],
                        budget_description=data['budget_description'],
                        budget_master=budget_master)

        budget.save()

        start_date = date(datetime.now().year, datetime.now().month, 1)

        for key, value in data.iteritems():
            budget_category_id = re.match(r'budget_category_(\d+)', key)
            if budget_category_id and budget_category_id.group(1):
                budget_category = \
                    BudgetCategory.objects.get(
                        budget_category_id=budget_category_id.group(1))

                if budget_category:
                    try:
                        value = float(value)
                    except ValueError:
                        value = 0

                    budget_amount = \
                        BudgetAmount(budget=budget,
                                     budget_category=budget_category,
                                     budget_amount=float(value),
                                     start_date=start_date,
                                     end_date=None)

                    budget_amount.save()

        return True

    def edit_budget(self, data, budget_master):
        """
        start_date = date(datetime.now().year, datetime.now().month, 1)
        end_date = date(datetime.now().year, datetime.now().month,
                        calendar.monthrange(datetime.now().year,
                                            datetime.now().month)[1])
        """
        budget_input_fields = [{'regex': r'^budget_category_(\d+)$',
                                'future': False},
                               {'regex': r'^budget_category_(\d+)_future$',
                                'future': True}]
        budget = Budget.objects.get(pk=data['budget_id'])

        if not budget:
            return False

        budget.budget_name = data['budget_name']
        budget.budget_description = data['budget_description']
        budget.budget_master = budget_master

        budget.save()

        for budget_input_field in budget_input_fields:
            for key, value in data.iteritems():
                budget_category_id = re.match(budget_input_field['regex'], key)
                if budget_category_id and budget_category_id.group(1) and value:
                    self.update_budget_amounts(data['budget_id'],
                                               budget_category_id.group(1),
                                               Decimal(value),
                                               budget_input_field['future'])


        return True

    @staticmethod
    def update_budget_amounts(budget_id, budget_category_id, value,
                              future_value):

        today = datetime.now()
        next_month = date(today.year, today.month, 1) + relativedelta(months=1)
        prev_month = date(today.year, today.month, 1) - relativedelta(months=1)

        if future_value:
            start_this_month = date(next_month.year, next_month.month, 1)
            end_this_month = date(next_month.year, next_month.month,
                                  calendar.monthrange(next_month.year,
                                                      next_month.month)[1])

            end_last_month = date(today.year, today.month,
                                  calendar.monthrange(today.year,
                                                      today.month)[1])
        else:
            start_this_month = date(today.year, today.month, 1)
            end_this_month = date(today.year, today.month,
                                  calendar.monthrange(today.year,
                                                      today.month)[1])

            end_last_month = date(prev_month.year, prev_month.month,
                                  calendar.monthrange(prev_month.year,
                                                      prev_month.month)[1])

        budget_amount = \
            BudgetAmount.objects.filter(
                Q(budget_id=budget_id),
                Q(budget_category=budget_category_id),
                Q(start_date__lte=start_this_month),
                Q(Q(end_date__gte=end_this_month) | Q(end_date=None)))

        if budget_amount:
            budget_amount = budget_amount[0]

        if not budget_amount and value:
            budget_amount = \
                BudgetAmount(budget_id=budget_id,
                             budget_category_id=budget_category_id,
                             budget_amount=value,
                             start_date=start_this_month,
                             end_date=None)
            budget_amount.save()

        if budget_amount and value != budget_amount.budget_amount:
            budget_amount.end_date = end_last_month
            budget_amount.save()

            if value:
                budget_amount = \
                    BudgetAmount(budget_id=budget_id,
                                 budget_category_id=budget_category_id,
                                 budget_amount=value,
                                 start_date=start_this_month,
                                 end_date=None)
                budget_amount.save()

