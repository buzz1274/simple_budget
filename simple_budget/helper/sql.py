from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DatabaseError
from simple_budget.settings import DATABASES

class SQL(object):

    db = None
    db_session = None
    budget_category = None
    transaction = None
    transaction_line = None
    connection_active = False

    def __init__(self):
        """
        creates a db connecton using sqlalchemy
        :return:
        """
        try:
            self.db = create_engine('postgresql://%s:%s@%s:%s/%s' %
                                    (DATABASES['default']['USER'],
                                     DATABASES['default']['PASSWORD'],
                                     DATABASES['default']['HOST'],
                                     DATABASES['default']['PORT'],
                                     DATABASES['default']['NAME'],))

            session = sessionmaker()
            session.configure(bind=self.db)

            self.db_session = session()

            self.budget_category = Table('budget_category', MetaData(),
                                         autoload=True, autoload_with=self.db)

            self.budget_type = Table('budget_type', MetaData(),
                                     autoload=True, autoload_with=self.db)

            self.transaction = Table('transaction', MetaData(),
                                     autoload=True, autoload_with=self.db)

            self.transaction_category = Table('transaction_category', MetaData(),
                                              autoload=True,
                                              autoload_with=self.db)

            self.transaction_line = Table('transaction_line', MetaData(),
                                          autoload=True, autoload_with=self.db)

        except DatabaseError:
            self.db = False
