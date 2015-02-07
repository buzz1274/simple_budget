from __future__ import unicode_literals
from django.db import models
from account_type import AccountType
from simple_budget.helper.sql import SQL
from sqlalchemy import func, and_
from decimal import Decimal
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import math


class Account(models.Model):
    """
    account model
    """
    account_id = models.AutoField(primary_key=True)
    account_name = models.TextField(blank=True)
    account_notes = models.TextField(blank=True, null=True)
    account_type = models.ForeignKey(AccountType, blank=True, null=True)

    class Meta:
        db_table = 'account'


    @staticmethod
    def debt():
        """
        gets balance for all debt related account types
        :return:
        """
        today = datetime.now()
        sql = SQL()

        balance_max_date = \
            sql.db_session.query(sql.account_balance.c.account_id,
                                 func.max(sql.account_balance.c.account_balance_date).
                                 label('max_balance_date')). \
                group_by(sql.account_balance.c.account_id).subquery()

        balance_last_month = \
            sql.db_session.query(sql.account_balance.c.account_id,
                                 func.max(sql.account_balance.c.account_balance).
                                    label('last_month_balance')).\
                filter(sql.account_balance.c.account_balance_date <= '2015-01-31').\
                filter(sql.account_balance.c.account_balance_date >= '2015-01-01').\
                group_by(sql.account_balance.c.account_id).subquery()

        balance_last_year = \
            sql.db_session.query(sql.account_balance.c.account_id,
                                 func.max(sql.account_balance.c.account_balance).
                                 label('last_year_balance')). \
                filter(sql.account_balance.c.account_balance_date <= '2014-01-31'). \
                filter(sql.account_balance.c.account_balance_date >= '2014-01-01'). \
                group_by(sql.account_balance.c.account_id).subquery()

        debts = sql.db_session.query(
                    sql.account.c.account_id,
                    sql.account.c.account_name,
                    sql.account_balance.c.account_balance.\
                        label('current_balance'),
                    balance_last_month.c.last_month_balance,
                    balance_last_year.c.last_year_balance). \
                outerjoin(balance_max_date,
                          balance_max_date.c.account_id ==
                          sql.account.c.account_id). \
                outerjoin(sql.account_balance,
                          and_(sql.account_balance.c.account_id ==
                               sql.account.c.account_id,
                               sql.account_balance.c.account_balance_date ==
                               balance_max_date.c.max_balance_date)).\
                outerjoin(balance_last_month,
                          balance_last_month.c.account_id ==
                          sql.account.c.account_id). \
                outerjoin(balance_last_year,
                          balance_last_year.c.account_id ==
                          sql.account.c.account_id). \
                group_by(sql.account.c.account_id,
                             sql.account.c.account_name,
                             sql.account_balance.c.account_balance,
                             balance_last_month.c.last_month_balance,
                             balance_last_year.c.last_year_balance).\
                order_by(sql.account.c.account_name.asc())

        if not debts:
            return [False, False]
        else:
            totals = {'current_balance': 0,
                      'last_month_balance': 0,
                      'last_month_balance_diff': 0,
                      'last_year_balance': 0,
                      'last_year_balance_diff': 0,
                      'avg_debt_repayment': 0,
                      'last_month_debt_repayment': 0}

            for debt in debts:
                totals['current_balance'] += debt.current_balance
                totals['last_month_balance'] += debt.last_month_balance
                totals['last_month_balance_diff'] = \
                    totals['current_balance'] - totals['last_month_balance']
                totals['last_year_balance'] += debt.last_year_balance
                totals['last_year_balance_diff'] = \
                    totals['current_balance'] - totals['last_year_balance']

            if totals['last_year_balance_diff']:
                totals['avg_debt_repayment'] = \
                    abs(totals['last_year_balance_diff'] / 12). \
                        quantize(Decimal('.01'))

                totals['avg_debt_repayment_date'] = \
                    date(today.year, today.month, 1) + \
                          relativedelta(months=int(math.ceil(totals['current_balance'] /
                                                             totals['avg_debt_repayment'])))

            if totals['last_month_balance_diff'] < 0:
                totals['last_month_debt_repayment'] = \
                    abs(totals['last_month_balance_diff'])

                totals['last_month_debt_repayment_date'] = \
                    date(today.year, today.month, 1) + \
                    relativedelta(months=int(math.ceil(totals['current_balance'] /
                                                       totals['last_month_debt_repayment'])))

            return [debts, totals]
