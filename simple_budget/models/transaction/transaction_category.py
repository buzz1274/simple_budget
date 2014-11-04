from __future__ import unicode_literals
from django.db import models
from simple_budget.helper.sql import SQL
from simple_budget.models.budget.budget_category import BudgetCategory
from sqlalchemy.orm import aliased
from sqlalchemy import func, case

class TransactionCategory(models.Model):
    """
    transaction category model
    """
    transaction_category_id = models.AutoField(primary_key=True)
    transaction_category_parent = models.ForeignKey('self', blank=True,
                                                    null=True)
    budget_category = models.ForeignKey('BudgetCategory', blank=True, null=True)
    transaction_category = models.TextField(blank=True)

    class Meta:
        db_table = 'transaction_category'

    @staticmethod
    def transaction_category_mapping():
        """
        returns budget/transaction category mapping
        :return:
        """
        sql = SQL()
        parent_transaction_category = aliased(sql.transaction_category)

        transaction_categories = \
            sql.db_session.query(
                sql.transaction_category.c.transaction_category_id,
                sql.budget_type.c.budget_type,
                sql.budget_category.c.budget_category_id,
                sql.budget_category.c.budget_category,
                case([(parent_transaction_category.c.transaction_category.isnot(None),
                       func.CONCAT(parent_transaction_category.c.transaction_category,
                                   ' >> ',
                                   sql.transaction_category.c.transaction_category))
                     ], else_=sql.transaction_category.c.transaction_category). \
                label('category'),
                sql.transaction_category.c.budget_category_id). \
                outerjoin(sql.budget_category,
                          sql.transaction_category.c.budget_category_id ==
                          sql.budget_category.c.budget_category_id). \
                outerjoin(parent_transaction_category,
                          sql.transaction_category.c.transaction_category_parent_id ==
                          parent_transaction_category.c.transaction_category_id). \
                outerjoin(sql.budget_type,
                          sql.budget_type.c.budget_type_id ==
                          sql.budget_category.c.budget_type_id). \
                order_by(case([(parent_transaction_category.c.transaction_category.isnot(None),
                                func.CONCAT(parent_transaction_category.c.transaction_category,
                                            ' >> ',
                                            sql.transaction_category.c.transaction_category))
                              ], else_=sql.transaction_category.c.transaction_category)).\
                order_by(sql.budget_type.c.ordering.asc().nullsfirst()). \
                order_by(sql.budget_category.c.budget_category.asc().nullsfirst())

        return transaction_categories
