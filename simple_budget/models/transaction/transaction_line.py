from __future__ import unicode_literals
from django.db import models
from sqlalchemy.sql.expression import between
from sqlalchemy import desc, asc, func, case
from sqlalchemy.orm import aliased
from simple_budget.models.transaction.transaction_category import \
    TransactionCategory
from simple_budget.helper.sql import SQL


class TransactionLine(models.Model):
    """
    transaction line model
    """
    transaction_line_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey("Transaction", blank=True, null=True)
    transaction_category = \
        models.ForeignKey(TransactionCategory, blank=True, null=True)
    amount = \
        models.DecimalField(max_digits=7, decimal_places=2, blank=True,
                            null=True)

    class Meta:
        db_table = 'transaction_line'

    @staticmethod
    def transaction_lines(start_date, end_date, sort):
        """
        retrieves a list of transaction lines for the specified dates
        :return:
        """
        sql = SQL()
        sort_order = {0: [sql.transaction.c.transaction_date],
                      2: ['category'],
                      4: [sql.budget_category.c.budget_category],
                      6: [sql.transaction_line.c.amount],
                      8: [sql.account.c.account_name]}

        try:
            sort = int(sort)
            sort_lookup = sort - (sort % 2)
            sort_order[sort_lookup]
        except (ValueError, IndexError, TypeError):
            sort = 0
            sort_lookup = 0

        parent_transaction_category = aliased(sql.transaction_category)

        transaction_lines = sql.db_session.query(
            sql.transaction_line.c.transaction_line_id.label('id'),
            sql.account.c.account_name,
            sql.account.c.account_id,
            sql.budget_category.c.budget_category,
            sql.transaction.c.transaction_date, sql.transaction_line.c.amount,
            case([(parent_transaction_category.c.transaction_category.isnot(None),
                   func.CONCAT(parent_transaction_category.c.transaction_category,
                               ' >> ',
                               sql.transaction_category.c.transaction_category))
                 ], else_=sql.transaction_category.c.transaction_category). \
                label('category')).\
            join(sql.transaction,
                 sql.transaction.c.transaction_id==
                 sql.transaction_line.c.transaction_id). \
            filter(sql.budget_category.c.budget_category_id==
                   sql.transaction_category.c.budget_category_id). \
            filter(between(sql.transaction.c.transaction_date, start_date,
                           end_date)). \
            join(sql.transaction_category,
                 sql.transaction_category.c.transaction_category_id==
                 sql.transaction_line.c.transaction_category_id). \
            join(sql.account,
                 sql.account.c.account_id==
                 sql.transaction.c.account_id). \
            outerjoin(parent_transaction_category,
                      sql.transaction_category.c.transaction_category_parent_id ==
                      parent_transaction_category.c.transaction_category_id).\
            filter(sql.transaction_category.c.transaction_category != 'Holding')

        if sort % 2:
            transaction_lines = \
                transaction_lines.order_by(desc(sort_order[sort_lookup][0]))
        else:
            transaction_lines = \
                transaction_lines.order_by(asc(sort_order[sort_lookup][0]))

        return [sort, transaction_lines]



