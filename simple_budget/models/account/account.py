from __future__ import unicode_literals
from django.db import models
from account_type import AccountType
from simple_budget.helper.sql import SQL
from sqlalchemy import func, and_, or_
from decimal import Decimal
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import math
import calendar


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
    def account_balances(account_type):
        """
        get account balances of the supplied type
        :param type:
        :return:
        """
        today = datetime.now()
        sql = SQL()

        start_last_month = date(today.year, today.month, 1) - relativedelta(months=1)
        end_last_month = date(start_last_month.year, start_last_month.month,
                              calendar.monthrange(start_last_month.year,
                                                  start_last_month.month)[1])

        start_last_year = date(today.year, today.month, 1) - relativedelta(months=12)
        end_last_year = date(start_last_year.year, start_last_year.month,
                             calendar.monthrange(start_last_year.year,
                                                 start_last_year.month)[1])

        print start_last_year, end_last_year

        balance_max_date = \
            sql.db_session.query(sql.account_balance.c.account_id,
                                 func.max(sql.account_balance.c.account_balance_date).
                                 label('max_balance_date')). \
                group_by(sql.account_balance.c.account_id).subquery()

        balance_last_month = \
            sql.db_session.query(sql.account_balance.c.account_id,
                                 func.max(sql.account_balance.c.account_balance).
                                 label('last_month_balance')). \
                filter(sql.account_balance.c.account_balance_date <= end_last_month). \
                filter(sql.account_balance.c.account_balance_date >= start_last_month). \
                group_by(sql.account_balance.c.account_id).subquery()

        balance_last_year = \
            sql.db_session.query(sql.account_balance.c.account_id,
                                 func.max(sql.account_balance.c.account_balance).
                                 label('last_year_balance')). \
                filter(sql.account_balance.c.account_balance_date <= end_last_year). \
                filter(sql.account_balance.c.account_balance_date >= start_last_year). \
                group_by(sql.account_balance.c.account_id).subquery()

        account_balances = sql.db_session.query(
                    sql.account.c.account_id,
                    sql.account.c.account_name,
                    sql.account_type.c.account_type,
                    sql.account_balance.c.account_balance. \
                        label('current_balance'),
                    balance_last_month.c.last_month_balance,
                    balance_last_year.c.last_year_balance). \
            join(sql.account_type,
                 sql.account_type.c.account_type_id ==
                 sql.account.c.account_type_id). \
            outerjoin(balance_max_date,
                      balance_max_date.c.account_id ==
                      sql.account.c.account_id). \
            outerjoin(sql.account_balance,
                      and_(sql.account_balance.c.account_id ==
                           sql.account.c.account_id,
                           sql.account_balance.c.account_balance_date ==
                           balance_max_date.c.max_balance_date)). \
            outerjoin(balance_last_month,
                      balance_last_month.c.account_id ==
                      sql.account.c.account_id). \
            outerjoin(balance_last_year,
                      balance_last_year.c.account_id ==
                      sql.account.c.account_id). \
            group_by(sql.account.c.account_id,
                     sql.account.c.account_name,
                     sql.account_type.c.account_type,
                     sql.account_type.c.ordering,
                     sql.account_balance.c.account_balance,
                     balance_last_month.c.last_month_balance,
                     balance_last_year.c.last_year_balance). \
            order_by(sql.account_type.c.ordering.asc(),
                     sql.account.c.account_name.asc())

        if account_type == 'debt':
            account_balances = account_balances.filter(
                or_(sql.account_type.c.account_type=='Credit Card',
                    sql.account_type.c.account_type=='Loan'))

        return account_balances

    @staticmethod
    def account_balance_summary(account_type=None):
        """
        get a summary of all account balances
        :param account_type:
        :return:
        """
        sql = SQL()
        account_balances = sql.db_session.query(
                    sql.account_balance.c.account_balance_date,
                    func.sum(sql.account_balance.c.account_balance).\
                        label('balance')).\
            join(sql.account,
                 sql.account.c.account_id == sql.account_balance.c.account_id). \
            join(sql.account_type,
                 sql.account_type.c.account_type_id ==
                 sql.account.c.account_type_id). \
            group_by(sql.account_balance.c.account_balance_date).\
            order_by(sql.account_balance.c.account_balance_date.desc())

        print account_balances

        if account_type == 'debt':
            account_balances = account_balances.filter(
                or_(sql.account_type.c.account_type=='Credit Card',
                    sql.account_type.c.account_type=='Loan'))

        return account_balances

    def debt(self):
            """
            gets balance for all debt related account types
            :return:
            """
            today = datetime.now()
            account_balances = self.account_balances(account_type='debt')

            if not account_balances:
                return [False, False]
            else:
                totals = {'current_balance': 0,
                          'last_month_balance': 0,
                          'last_month_balance_diff': 0,
                          'last_year_balance': 0,
                          'last_year_balance_diff': 0,
                          'avg_debt_repayment': 0,
                          'last_month_debt_repayment': 0}

                for account_balance in account_balances:
                    if account_balance.current_balance:
                        totals['current_balance'] += \
                            account_balance.current_balance

                    if account_balance.last_month_balance:
                        totals['last_month_balance'] += \
                            account_balance.last_month_balance
                        totals['last_month_balance_diff'] = \
                            totals['current_balance'] - totals['last_month_balance']

                    if account_balance.last_year_balance:
                        totals['last_year_balance'] += \
                            account_balance.last_year_balance
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

                return [account_balances, totals]
