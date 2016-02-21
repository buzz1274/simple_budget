from __future__ import unicode_literals
from django.db import models
from simple_budget.models.transaction.transaction_line import TransactionLine
from simple_budget.models.account.account import Account
from django.conf import settings
from django.db import transaction as db_transaction
from django.db import DatabaseError
import os
import subprocess
import time


class Transaction(models.Model):
    """
    transaction model
    """
    transaction_id = models.AutoField(primary_key=True)
    transaction_date = models.DateField(null=False, blank=False)
    account = models.ForeignKey(Account, blank=True, null=True)

    class Meta:
        db_table = 'transaction'

    @db_transaction.atomic
    def add_edit_transaction(self, action, data):
        """
        :param action: add|edit
        :param data: transaction data
        :return: boolean
        """
        if action == 'edit':
            self.delete_transaction(data)

        new_transaction = Transaction(transaction_date=data['transaction_date'],
                                      account_id=data['account_id'],)
        new_transaction.save()

        if not new_transaction.pk:
            raise DatabaseError('Unable to save transaction')

        if (new_transaction.pk and data['transaction_category_id'] and
            data['amount']):
            transaction_line = \
                TransactionLine(transaction_id=
                                    new_transaction.pk,
                                transaction_category_id=
                                    data['transaction_category_id'],
                                amount=
                                    data['amount'])

            transaction_line.save()

            if not transaction_line.pk:
                raise DatabaseError('Unable to save transaction line')

    @db_transaction.atomic
    def delete_transaction(self, data):
        """
        delete a transaction and all associated transaction lines
        :param data: transaction data
        :return: boolean
        """
        try:
            transaction_line = \
                TransactionLine.objects.filter(
                    pk=data['transaction_line_id'])[0]
        except (IndexError, KeyError):
            raise DatabaseError('invalid transaction line')

        TransactionLine.objects.filter(
            transaction_id=transaction_line.transaction_id).delete()
        Transaction.objects.filter(
            transaction_id=transaction_line.transaction_id).delete()

    @staticmethod
    def process_upload_quicken_file(quicken_file):
        """
        saves and process the uploaded quicken file
        :param quicken_file:
        :return: boolean
        """
        filename = settings.TEMP_SAVE_PATH + quicken_file.name.lower()

        with open(filename, 'w+') as destination:
            for chunk in quicken_file.chunks():
                destination.write(chunk)

        if not os.path.isfile(filename):
            return False
        else:
            subprocess.Popen(['nohup', settings.PYTHON_PATH,
                              '%s/simple_budget/scripts/qif_file_parser.py' %
                                (settings.BASE_DIR,),
                              '-p', filename])
            time.sleep(5)

            return True
