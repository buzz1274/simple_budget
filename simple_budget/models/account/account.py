from __future__ import unicode_literals
from django.db import models
from account_type import AccountType
from simple_budget.helper.sql import SQL
from sqlalchemy import func, asc, or_
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
    account_hidden = models.BooleanField(blank=False, null=False, default=False)
    account_type = models.ForeignKey(AccountType, blank=True, null=True)

    class Meta:
        db_table = 'account'

    @staticmethod
    def accounts(account_type):
        """
        get account balances of the supplied type
        :param type:
        :return:
        """
        sql = SQL()

        accounts = sql.db_session.query(
                    sql.account.c.account_id,
                    sql.account.c.account_hidden,
                    sql.account.c.account_name,
                    sql.account_type.c.account_type). \
            join(sql.account_type,
                 sql.account_type.c.account_type_id ==
                 sql.account.c.account_type_id).\
            group_by(sql.account.c.account_id,
                     sql.account.c.account_name,
                     sql.account_type.c.account_type,
                     sql.account_type.c.ordering). \
            order_by(sql.account_type.c.ordering.asc(),
                     sql.account.c.account_name.asc())

        if account_type == 'debt':
            accounts = accounts.filter(
                or_(sql.account_type.c.account_type=='Credit Card',
                    sql.account_type.c.account_type=='Loan',
                    sql.account_type.c.account_type=='Store Card'))

        return accounts

    @staticmethod
    def account_balance_summary(account_type=None, account_id=None):
        """
        get a summary of all account balances
        :param account_type:
        :return:
        """
        sql = SQL()
        account_balances = sql.db_session.query(
                    func.date_trunc('month', sql.transaction.c.transaction_date).\
                        label('date'),
                    func.sum(sql.transaction_line.c.amount).\
                        label('balance')).\
            join(sql.transaction_line,
                 sql.transaction_line.c.transaction_id ==
                 sql.transaction.c.transaction_id). \
            join(sql.account,
                 sql.account.c.account_id ==
                 sql.transaction.c.account_id). \
            join(sql.account_type,
                 sql.account_type.c.account_type_id ==
                 sql.account.c.account_type_id). \
            group_by('date').\
            order_by(asc('date'))

        if account_id:
            account_balances = account_balances.filter(
                sql.account.c.account_id == account_id)

        if account_type == 'debt' and not account_id:
            account_balances = account_balances.filter(
                or_(sql.account_type.c.account_type=='Credit Card',
                    sql.account_type.c.account_type=='Loan',
                    sql.account_type.c.account_type=='Store Card'))

        #loop through all balances and fill in any gaps in the date
        #with the balance for the previous month

        return account_balances

    def debt_balance_summary(self):
        """
        gets summary for last 12 months debt balances
        :return:
        """
        debt_balances = []
        balances = self.account_balance_summary(account_type='debt')

        if balances:
            current_balance = 0
            start_this_month = date(datetime.now().year,
                                    datetime.now().month, 1)
            start_last_year = date(datetime.now().year,
                                   datetime.now().month, 1) - \
                              relativedelta(months=11)

            for balance in balances:
                current_balance = Decimal(current_balance - balance.balance).\
                                    quantize(Decimal('.01'))

                if (str(start_last_year) <=
                    str(balance.date.strftime('%Y-%m-%d')) <=
                    str(start_this_month)):
                    debt_balances.append(
                        {'date': balance.date.strftime('%Y-%m-%d'),
                         'balance': str(current_balance)})

        return debt_balances

    def debt(self):
        """
        gets balance for all debt related account types
        :return:
        """
        today = datetime.now()

        start_this_month = date(today.year, today.month, 1)
        start_last_month = date(today.year, today.month, 1) - \
                           relativedelta(months=1)
        start_last_year = date(start_this_month.year,
                               start_this_month.month, 1) - \
                          relativedelta(months=11)

        accounts = self.accounts(account_type='debt')

        if not accounts:
            return [False, False]
        else:
            account_balances = []
            totals = {'current_balance': 0,
                      'last_month_balance': 0,
                      'last_month_balance_diff': 0,
                      'today': today,
                      'last_month_date': start_last_month,
                      'last_year_date': start_last_year,
                      'last_year_balance': 0,
                      'last_year_balance_diff': 0,
                      'avg_debt_repayment': 0,
                      'last_month_debt_repayment': 0}

            for account in accounts:
                if not account.account_hidden:
                    current_balance = 0
                    balances = \
                        self.account_balance_summary(
                            account_id=account.account_id)

                    if not balances:
                        if current_balance:
                            account_balances['current_balance'] = \
                                current_balance
                        else:
                            account_balances['current_balance'] = 0
                    else:
                        for balance in balances:
                            current_balance = \
                                Decimal(current_balance - balance.balance).\
                                    quantize(Decimal('.01'))

                            if (str(balance.date.strftime('%Y-%m-%d')) ==
                                str(start_this_month)):
                                break

                            if (str(balance.date.strftime('%Y-%m-%d')) ==
                                str(start_last_month)):
                                last_month_balance = current_balance

                            if (str(balance.date.strftime('%Y-%m-%d')) ==
                                str(start_last_year)):
                                last_year_balance = current_balance

                    account_balances.append(
                        {'account_id': account.account_id,
                         'account_name': account.account_name,
                         'account_type': account.account_type,
                         'last_month_balance': last_month_balance,
                         'last_year_balance': last_year_balance,
                         'current_balance': current_balance})

                    last_month_balance = 0
                    last_year_balance = 0

            if account_balances:
                for account_balance in account_balances:
                    if account_balance['current_balance']:
                        totals['current_balance'] += \
                            account_balance['current_balance']

                    if account_balance['last_month_balance']:
                        totals['last_month_balance'] += \
                            account_balance['last_month_balance']

                    if account_balance['last_year_balance']:
                        totals['last_year_balance'] += \
                            account_balance['last_year_balance']

                totals['last_month_balance_diff'] = \
                    totals['last_month_balance'] - totals['current_balance']

                totals['last_year_balance_diff'] = \
                    totals['last_year_balance'] - totals['current_balance']

                if totals['last_year_balance_diff'] > 0:
                    totals['avg_debt_repayment'] = \
                        abs(totals['last_year_balance_diff'] / 12). \
                            quantize(Decimal('.01'))

                    totals['avg_debt_repayment_date'] = \
                        date(today.year, today.month, 1) + \
                        relativedelta(months=int(math.ceil(totals['current_balance'] /
                                                           totals['avg_debt_repayment'])))

                if totals['last_month_balance_diff'] > 0:
                    totals['last_month_debt_repayment'] = \
                        abs(totals['last_month_balance_diff'])

                    totals['last_month_debt_repayment_date'] = \
                        date(today.year, today.month, 1) + \
                        relativedelta(months=int(math.ceil(totals['current_balance'] /
                                                           totals['last_month_debt_repayment'])))

            return [account_balances, totals]