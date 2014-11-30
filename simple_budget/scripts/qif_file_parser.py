#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
quicken qif parser.
File format details taken from http://en.wikipedia.org/wiki/Quicken_Interchange_Format
"""
from datetime import datetime
from optparse import OptionParser
import re
import sys
import os.path
import yaml
import django

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../simple_budget'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simple_budget.settings")

from simple_budget.helper.sql import SQL
from simple_budget.models.transaction.qif_parser import QIFParser

class QuickenException(Exception):
    pass

class Quicken(object):
    CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../config.yaml'
    sql = None
    transfer_accounts = None
    references = None

    def __init__(self):
        """
        init
        """
        django.setup()
        self.sql = SQL()
        self.read_config()

    def main(self):
        """
        entry point when running script from command line
        """
        parser = OptionParser()
        parser.add_option("-p", "--path", dest="path", metavar="path",
                          help="path to quicken file")

        (options, args) = parser.parse_args()

        if not options.path:
            parser.print_help()
        else:
            if not os.path.isfile(options.path):
                raise QuickenException("QIF file does not exist")

            if not self.sql.db:
                raise QuickenException("No Database Connection")

            try:
                qif_parser = QIFParser()
                qif_parser.parse_status = 'in_progress'
                qif_parser.save()

                self.clean_db()
                self.parse_quicken_file(options.path)
                self.clean_childless_transactions()
                self.delete_quicken_file(options.path)
                self.sql.db_session.commit()

                qif_parser.parse_status = 'complete'
                qif_parser.save()

            except Exception, ex:
                self.sql.db_session.rollback()

                qif_parser.parse_status = 'failed'
                qif_parser.save()

                raise Exception(ex)

    def read_config(self):
        """
        reads config file, connects to DB and sets appropriate
        class variables
        """
        with open(self.CONFIG_PATH) as f:
            config = yaml.load(f)

        if 'accounts' in config:
            self.transfer_accounts = config['accounts']

        if 'references' in config:
            self.references = config['references']

    def clean_db(self):
        """
        truncates all table and resets all sequences
        """
        self.sql.db_session.execute(
            "ALTER SEQUENCE transaction_id RESTART WITH 1")
        self.sql.db_session.execute(
            "ALTER SEQUENCE transaction_line_id RESTART WITH 1")
        self.sql.db_session.execute(
            "DELETE FROM transaction_line CASCADE")
        self.sql.db_session.execute(
            "DELETE FROM transaction CASCADE")

    def parse_quicken_file(self, quicken_file):
        """
        parse quicken qif file for transactions
        """
        with open(quicken_file, 'r') as f:
            transaction_found = False
            transaction = {}

            for line in f:
                if line[0] == 'D':
                    try:
                        date = datetime.strptime(line[1:].strip(), '%d/%m/%y')
                        transaction_found = True
                        transaction = {'date': date.strftime('%Y-%m-%d'),
                                       'split': [], 'category': None,
                                       'reference': None,
                                       'sub_category': None}
                    except ValueError:
                        transaction = {}
                        transaction_found = False

                elif transaction_found and line[0] == 'T':
                    transaction['amount'] = self.parse_amount(line[1:])

                elif transaction_found and line[0] == 'L':
                    transaction['category'], transaction['sub_category'] =\
                        self.split_category(line[1:])

                elif transaction_found and line[0] == 'S':
                    category, sub_category = self.split_category(line[1:])

                elif transaction_found and line[0] == 'N':
                    transaction['reference'] = line[1:].strip()

                elif transaction_found and line[0] == '$' and category:
                    transaction['split'].append(
                        {'category': category,
                         'sub_category': sub_category,
                         'amount': self.parse_amount(line[1:])})
                    category = None
                    sub_category = None

                elif line[0] == '^':
                    if transaction:
                        if not transaction['split']:
                            transaction['split'].append(
                                {'category': transaction['category'],
                                 'sub_category': transaction['sub_category'],
                                 'amount': transaction['amount']})

                        transaction_id = \
                            self.save_transaction(transaction['date'])

                        for transaction_line in transaction['split']:
                            if (transaction_line['category'] and
                                (not transaction['reference'] or
                                 transaction['reference'] != 'xxx') and
                                (not re.match('\[', transaction_line['category']) or
                                 transaction_line['category'] in self.transfer_accounts or
                                 (transaction['reference'] and
                                  transaction['reference'] in self.references))):

                                if transaction['reference'] in self.references:
                                    transaction_line['sub_category'] = None
                                    transaction_line['category'] = \
                                        self.references[transaction['reference']]

                                transaction_category_id = \
                                    self.save_category(
                                        transaction_line['sub_category'],
                                        transaction_line['category'])

                                self.save_transaction_line(
                                    transaction_id, transaction_category_id,
                                    transaction_line['amount'])

                    transaction_found = False
                    transaction = {}

    def save_transaction(self, transaction_date):
        """
        saves the transaction
        """
        return self.sql.db_session.execute(
                    self.sql.transaction.insert(). \
                    values(transaction_date=transaction_date). \
                    returning(self.sql.transaction.c.transaction_id)).scalar()

    def save_transaction_line(self, transaction_id, transaction_category_id, amount):
        """
        saves a transaction line
        @return integer transaction_line_id
        """
        return self.sql.db_session.execute(self.sql.transaction_line.insert(). \
            values(transaction_id=transaction_id,
                   transaction_category_id=transaction_category_id,
                   amount=amount). \
            returning(self.sql.transaction_line.c.transaction_line_id)).scalar()

    def save_category(self, transaction_category, parent_transaction_category):
        """
        saves the supplied transaction_category
        @return integer transaction_category_id
        """
        if not transaction_category:
            transaction_category = parent_transaction_category
            transaction_category_parent_id = None
        else:
            transaction_category_parent_id = \
                self.get_category_id(parent_transaction_category, None)

            if not transaction_category_parent_id:
                self.sql.db_session.execute(
                    self.sql.transaction_category.insert(). \
                    values(transaction_category=parent_transaction_category,
                           transaction_category_parent_id=None))

                transaction_category_parent_id = \
                    self.get_category_id(parent_transaction_category, None)

        transaction_category_id = self.get_category_id(
                                        transaction_category,
                                        transaction_category_parent_id)

        if transaction_category_id:
            return transaction_category_id
        else:
            self.sql.db_session.execute(self.sql.transaction_category.insert().\
                            values(transaction_category=transaction_category,
                                   transaction_category_parent_id=
                                        transaction_category_parent_id))

            return self.get_category_id(transaction_category,
                                        transaction_category_parent_id)

    def get_category_id(self, transaction_category, transaction_category_parent_id):
        """
        gets the category id for the supplied category
        will return false if no matching category found.
        @return integer
        """
        return self.sql.db_session.query(
                        self.sql.transaction_category.c.transaction_category_id).\
                    filter(transaction_category ==
                           self.sql.transaction_category.c.transaction_category).\
                    filter(transaction_category_parent_id ==
                           self.sql.transaction_category.c.transaction_category_parent_id).\
                    scalar()

    def clean_childless_transactions(self):
        """
        deletes all transaction that have no transaction lines
        @todo determine why calling delete() on result throws an exception
              because this is pretty damn inefficient.
        """
        result = self.sql.db_session.query(self.sql.transaction). \
            outerjoin(self.sql.transaction_line,
                      self.sql.transaction.c.transaction_id==
                      self.sql.transaction_line.c.transaction_id). \
            filter(self.sql.transaction_line.c.transaction_line_id is None)

        for row in result:
            self.sql.db_session.execute(
                            self.sql.transaction.delete(). \
                            where(self.sql.transaction.c.transaction_id==
                                  row.transaction_id))

    @staticmethod
    def split_category(category):
        """
        splits category into category & sub category
        @return string
        """
        try:
            category = category.strip().split(':')
            sub_category = category[1].strip()
        except IndexError:
            sub_category = None

        category = category[0].strip()

        return category, sub_category

    @staticmethod
    def delete_quicken_file(quicken_file):
        """
        deletes the processed quicken file
        """
        try:
            os.remove(quicken_file)
        except OSError:
            pass

    @staticmethod
    def parse_amount(amount):
        """
        strips invalid chars from amount
        @return float
        """
        return float(re.sub('[^0-9\-\.]', '', amount))

    @staticmethod
    def display_message(message, message_type="normal"):
        """
        displays the passed message with colour control characters
        """
        if message_type == 'error':
            #red
            control_char = '\033[91m'
        else:
            #white
            control_char = '\033[0m'

        end_control_char = '\033[0m'

        print "%s%s%s" % (control_char, message, end_control_char)

if __name__ == '__main__':
    try:
        Quicken().main()
    except Exception, e:
        Quicken.display_message(e, 'error')

