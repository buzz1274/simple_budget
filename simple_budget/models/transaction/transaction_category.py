from __future__ import unicode_literals
from django.db import models
from simple_budget.helper.sql import SQL
from sqlalchemy.orm import aliased
from sqlalchemy import func, case, desc, asc

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
    def transaction_category_mapping(sort, budget_category_id):
        """
        returns budget/transaction category mapping
        :return:
        """
        sql = SQL()
        parent_transaction_category = aliased(sql.transaction_category)

        sort_order = {0: ['category'],
                      2: [sql.budget_category.c.budget_category],
                      4: [sql.budget_type.c.budget_type]}

        try:
            sort = int(sort)
            sort_lookup = sort - (sort % 2)
            sort_order[sort_lookup]
        except (ValueError, IndexError, TypeError):
            sort = 0
            sort_lookup = 0

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
                          sql.budget_category.c.budget_type_id)

        if budget_category_id:
            if budget_category_id == '0':
                budget_category_id = None
            else:
                budget_category_id = int(budget_category_id)

            transaction_categories = \
                transaction_categories.filter(
                    sql.budget_category.c.budget_category_id==budget_category_id)

        if sort % 2:
            transaction_categories = \
                transaction_categories.order_by(desc(sort_order[sort_lookup][0]))
        else:
            transaction_categories = \
                transaction_categories.order_by(asc(sort_order[sort_lookup][0]))

        return [sort, transaction_categories]
