from __future__ import unicode_literals
from django.db import models
from simple_budget.helper.sql import SQL
from sqlalchemy import func, desc, asc
from budget_type import BudgetType


class BudgetCategory(models.Model):
    """
    budget category model
    """
    budget_category_id = models.AutoField(primary_key=True)
    budget_category = models.TextField(blank=True)
    budget_type = models.ForeignKey(BudgetType, blank=True, null=True)

    class Meta:
        db_table = 'budget_category'
        app_label = 'simple_budget'

    @staticmethod
    def budget_categories(sort):
        """
        retrieves a dict of all budget categories
        :return:
        """
        sql = SQL()

        sort_order = {0: [sql.budget_category.c.budget_category],
                      2: [sql.budget_type.c.budget_type],
                      4: ['tc_count'],}

        try:
            sort = int(sort)
            sort_lookup = sort - (sort % 2)
            sort_order[sort_lookup]
        except (ValueError, IndexError, TypeError):
            sort = 0
            sort_lookup = 0

        transaction_categories = sql.db_session.query(
                sql.transaction_category.c.budget_category_id,
                func.COUNT(sql.transaction_category.c.budget_category_id).\
                    label('tc_count')).\
            group_by(sql.transaction_category.c.budget_category_id).subquery()

        budget_categories = sql.db_session.query(
                sql.budget_category.c.budget_category_id,
                sql.budget_type.c.budget_type,
                transaction_categories.c.tc_count,
                sql.budget_category.c.budget_category). \
            filter(sql.budget_type.c.budget_type_id==
                   sql.budget_category.c.budget_type_id). \
            filter(sql.budget_type.c.budget_type_id==
                   sql.budget_category.c.budget_type_id). \
            outerjoin(transaction_categories,
                      transaction_categories.c.budget_category_id==
                      sql.budget_category.c.budget_category_id)

        if sort % 2:
            budget_categories = \
                budget_categories.order_by(desc(sort_order[sort_lookup][0]))
        else:
            budget_categories = \
                budget_categories.order_by(asc(sort_order[sort_lookup][0]))

        return [sort, budget_categories]