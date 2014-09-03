#!/usr/bin/python
"""
quicken qif parser.
File format details taken from http://en.wikipedia.org/wiki/Quicken_Interchange_Format
"""
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import re
import sys
import os.path
import ConfigParser

class QuickenException(Exception):
    pass


class Quicken(object):
    CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/config.ini'
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
                          'filename': sys.argv[1]}

    def _parse(self):
        """
        parse quicken qif file for transactions
        """
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
                                   'sub_category': None}
                except ValueError:
                    transaction = {}
                    transaction_found = False

            elif transaction_found and line[0] == 'T':
                transaction['amount'] = self._parse_amount(line[1:])

            elif transaction_found and line[0] == 'L':
                transaction['category'], transaction['sub_category'] = self._split_category(line[1:])

            elif transaction_found and line[0] == 'S':
                category, sub_category = self._split_category(line[1:])

            elif transaction_found and line[0] == '$' and category:
                transaction['split'].append({'category': category,
                                             'sub_category': sub_category,
                                             'amount': self._parse_amount(line[1:])})
                category = None
                sub_category = None

            elif line[0] == '^':
                if transaction:
                    if not transaction['split']:
                        transaction['split'].append({'category': transaction['category'],
                                                     'sub_category': transaction['sub_category'],
                                                     'amount': transaction['amount']})

                    transaction_id = self._save_transaction(transaction['date'])

                    for transaction_line in transaction['split']:
                        if (transaction_line['category'] and
                            (not re.match('\[', transaction_line['category']) or
                             transaction_line['category'] in self.transfer_accounts)):
                            transaction_category_id = self._save_category(transaction_line['sub_category'],
                                                                          transaction_line['category'])
                            self._save_transaction_line(transaction_id, transaction_category_id,
                                                        transaction_line['amount'])

                transaction_found = False
                transaction = {}

        self._clean_childless_transactions()
        self._mark_transactions_cleared()

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
        result = self.db.execute(self.transaction_table.insert(). \
                                 values(transaction_date=transaction_date). \
                                 returning(self.transaction_table.c.transaction_id))

        return result.scalar()

    def _save_transaction_line(self, transaction_id, transaction_category_id, amount):
        """
        saves a transaction line
        @return integer transaction_line_id
        """
        result = self.db.execute(self.transaction_line_table.insert(). \
                                 values(transaction_id=transaction_id,
                                        transaction_category_id=transaction_category_id,
                                        amount=amount). \
                                 returning(self.transaction_line_table.c.transaction_line_id))

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
                self.db.execute(self.transaction_category_table.insert(). \
                                values(transaction_category=parent_transaction_category,
                                       transaction_category_parent_id=None))

                transaction_category_parent_id = self._get_category_id(parent_transaction_category,
                                                                       None)

        transaction_category_id = self._get_category_id(transaction_category,
                                                        transaction_category_parent_id)

        if transaction_category_id:
            return transaction_category_id
        else:
            self.db.execute(self.transaction_category_table.insert(). \
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
        query = select([self.transaction_category_table.c.transaction_category_id]). \
                 where(self.transaction_category_table.c.transaction_category ==
                            transaction_category).\
                 where(self.transaction_category_table.c.transaction_category_parent_id ==
                            transaction_category_parent_id)

        return self.db.execute(query).scalar()

    def _reset_cleared_transactions(self):
        """
        resets all cleared transactions to be uncleared
        """
        pass

    def _mark_transactions_cleared(self):
        """
        marks all transaction as cleared
        """
        pass

    def _clean_childless_transactions(self):
        """
        deletes all transaction that have no transaction lines
        @todo determine why calling delete() on result throws an exception
              because this is pretty damn inefficient.
        """
        result = self.db_session.query(self.transaction_table). \
            outerjoin(self.transaction_line_table,
                      self.transaction_table.c.transaction_id==
                      self.transaction_line_table.c.transaction_id). \
            filter(self.transaction_line_table.c.transaction_line_id == None)

        for row in result:
            self.db.execute(self.transaction_table.delete(). \
                            where(self.transaction_table.c.transaction_id==row.transaction_id))

    def _clean_db(self):
        """
        truncates all table and resets all sequences
        """
        self.db.execute("ALTER SEQUENCE transaction_id RESTART WITH 1")
        self.db.execute("ALTER SEQUENCE transaction_line_id RESTART WITH 1")
        self.db.execute("DELETE FROM transaction_line CASCADE")
        self.db.execute("DELETE FROM transaction CASCADE")

    def _read_config(self):
        """
        reads config file, connects to DB and sets appropriate
        class variables
        """
        config = ConfigParser.ConfigParser()
        config.read(self.CONFIG_PATH)

        self.db_engine = config.get('DB', 'db_engine')
        self.db_user = config.get('DB', 'db_user')
        self.db_password = config.get('DB', 'db_password')
        self.db_host = config.get('DB', 'db_host')
        self.db_port = config.get('DB', 'db_port')
        self.db_name = config.get('DB', 'db_name')
        self.transfer_accounts = config.get('ACCOUNTS', 'accounts')

        self.db = create_engine('%s://%s:%s@%s:%s/%s' %
                                (self.db_engine, self.db_user,
                                 self.db_password, self.db_host,
                                 self.db_port, self.db_name))

        self.transaction_table = Table('transaction', MetaData(), autoload=True,
                                       autoload_with=self.db)
        self.transaction_category_table = Table('transaction_category', MetaData(), autoload=True,
                                                autoload_with=self.db)
        self.transaction_line_table = Table('transaction_line', MetaData(),
                                            autoload=True, autoload_with=self.db)

        Session = sessionmaker()
        Session.configure(bind=self.db)
        self.db_session = Session()

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