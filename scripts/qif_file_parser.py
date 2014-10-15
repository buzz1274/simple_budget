#!/usr/bin/python
"""
quicken qif parser.
File format details taken from http://en.wikipedia.org/wiki/Quicken_Interchange_Format
"""
from datetime import datetime
import re
import sys
import os.path
import yaml

sys.path.insert(0, '%s/../simple_budget/' %
                (os.path.dirname(os.path.realpath(__file__)),))
from helper.sql import SQL

class QuickenException(Exception):
    pass

class Quicken(object):
    CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + \
                  '/../simple_budget/config.yaml'
    arguments = {}
    db_user = None
    db_host = None
    db_password = None
    db_port = None
    db_engine = None
    db = None
    transaction_table = None
    transaction_category_table = None
    transaction_line_table = None

    def __init__(self):
        """
        init
        """
        self._read_config()
        self._parse_arguments()

        try:
            func = getattr(self, self.arguments['action'])
        except AttributeError:
            self._display_message("Invalid action(%s)" % (self.arguments['action'],), 'error')
        else:
            func()

    def _parse_arguments(self):
        """
        parses commandline arguments to determine
        @return dict
        """
        if len(sys.argv) < 2:
            sys.exit(self._display_message("Please supply a QIF filename", 'error'))
        if not os.path.isfile(sys.argv[1]):
            sys.exit(self._display_message("QIF file does not exist", 'error'))

        self.arguments = {'action': '_parse',
                          'clean_db': True,
                          'filename': sys.argv[1],
                          'delete_file': True}

    def _parse(self):
        """
        parse quicken qif file for transactions
        """
        try:
            self.sql.db_session.begin(subtransactions=True)
            if self.arguments['clean_db']:
                self._clean_db()
            else:
                self._reset_cleared_transactions()

            f = open(self.arguments['filename'], 'r')
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
                    transaction['amount'] = self._parse_amount(line[1:])

                elif transaction_found and line[0] == 'L':
                    transaction['category'], transaction['sub_category'] =\
                        self._split_category(line[1:])

                elif transaction_found and line[0] == 'S':
                    category, sub_category = self._split_category(line[1:])

                elif transaction_found and line[0] == 'N':
                    transaction['reference'] = line[1:].strip()

                elif transaction_found and line[0] == '$' and category:
                    transaction['split'].append(
                        {'category': category,
                         'sub_category': sub_category,
                         'amount': self._parse_amount(line[1:])})
                    category = None
                    sub_category = None

                elif line[0] == '^':
                    if transaction:
                        if not transaction['split']:
                            transaction['split'].append(
                                {'category': transaction['category'],
                                 'sub_category': transaction['sub_category'],
                                 'amount': transaction['amount']})

                        transaction_id = self._save_transaction(transaction['date'])

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
                                    self._save_category(transaction_line['sub_category'],
                                                        transaction_line['category'])

                                self._save_transaction_line(
                                    transaction_id, transaction_category_id,
                                    transaction_line['amount'])

                    transaction_found = False
                    transaction = {}

            self._clean_childless_transactions()
            self.sql.db_session.commit()

            if self.arguments['delete_file']:
                try:
                    os.remove(self.arguments['filename'])
                except OSError:
                    pass

        except Exception, e:
            self.sql.db_session.rollback()

    def _split_category(self, category):
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

    def _parse_amount(self, amount):
        """
        strips invalid chars from amount
        @return float
        """
        return float(re.sub('[^0-9\-\.]', '', amount))

    def _save_transaction(self, transaction_date):
        """
        saves the transaction
        """
        result = self.sql.db.execute(self.sql.transaction.insert(). \
                                     values(transaction_date=transaction_date). \
                                     returning(self.sql.transaction.c.transaction_id))

        return result.scalar()

    def _save_transaction_line(self, transaction_id, transaction_category_id, amount):
        """
        saves a transaction line
        @return integer transaction_line_id
        """
        result = self.sql.db.execute(self.sql.transaction_line.insert(). \
                                 values(transaction_id=transaction_id,
                                        transaction_category_id=transaction_category_id,
                                        amount=amount). \
                                 returning(self.sql.transaction_line.c.transaction_line_id))

        return result.scalar()

    def _save_category(self, transaction_category, parent_transaction_category):
        """
        saves the supplied transaction_category
        @return integer transaction_category_id
        """
        if not transaction_category:
            transaction_category = parent_transaction_category
            transaction_category_parent_id = None
        else:
            transaction_category_parent_id = self._get_category_id(parent_transaction_category,
                                                                   None)

            if not transaction_category_parent_id:
                self.sql.db.execute(self.sql.transaction_category.insert(). \
                                values(transaction_category=parent_transaction_category,
                                       transaction_category_parent_id=None))

                transaction_category_parent_id = self._get_category_id(parent_transaction_category,
                                                                       None)

        transaction_category_id = self._get_category_id(transaction_category,
                                                        transaction_category_parent_id)

        if transaction_category_id:
            return transaction_category_id
        else:
            self.sql.db.execute(self.sql.transaction_category.insert(). \
                            values(transaction_category=transaction_category,
                                   transaction_category_parent_id=transaction_category_parent_id))

            return self._get_category_id(transaction_category,
                                         transaction_category_parent_id)

    def _get_category_id(self, transaction_category, transaction_category_parent_id):
        """
        gets the category id for the supplied category
        will return false if no matching category found.
        @return integer
        """
        result = self.sql.db_session.query(
                        self.sql.transaction_category.c.transaction_category_id).\
                    filter(transaction_category ==
                           self.sql.transaction_category.c.transaction_category).\
                    filter(transaction_category_parent_id ==
                           self.sql.transaction_category.c.transaction_category_parent_id).\
                    scalar()

        return result

    def _clean_childless_transactions(self):
        """
        deletes all transaction that have no transaction lines
        @todo determine why calling delete() on result throws an exception
              because this is pretty damn inefficient.
        """
        result = self.sql.db_session.query(self.sql.transaction). \
            outerjoin(self.sql.transaction_line,
                      self.sql.transaction.c.transaction_id==
                      self.sql.transaction_line.c.transaction_id). \
            filter(self.sql.transaction_line.c.transaction_line_id == None)

        for row in result:
            self.sql.db.execute(self.sql.transaction.delete(). \
                            where(self.sql.transaction.c.transaction_id==row.transaction_id))

    def _clean_db(self):
        """
        truncates all table and resets all sequences
        """
        self.sql.db.execute("ALTER SEQUENCE transaction_id RESTART WITH 1")
        self.sql.db.execute("ALTER SEQUENCE transaction_line_id RESTART WITH 1")
        self.sql.db.execute("DELETE FROM transaction_line CASCADE")
        self.sql.db.execute("DELETE FROM transaction CASCADE")

    def _read_config(self):
        """
        reads config file, connects to DB and sets appropriate
        class variables
        """
        self.sql = SQL()
        with open(self.CONFIG_PATH) as f:
            config = yaml.load(f)

        if 'accounts' in config:
            self.transfer_accounts = config['accounts']

        if 'references' in config:
            self.references = config['references']

    def _display_message(self, message, message_type="normal"):
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
    Quicken()
