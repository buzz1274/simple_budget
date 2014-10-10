from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$',
        'simple_budget.views.views.index',
        name='index'),
    url(r'^budget/?$',
        'simple_budget.views.budget.budget.budget',
        name='index'),
    url(r'^transaction/category/(add|edit)/?([0-9]+)?/?$',
        'simple_budget.views.transaction.transaction.add_edit_transaction_category',
        name='budget_category'),
    url(r'^transaction/category/delete/([0-9]+)/?$',
        'simple_budget.views.transaction.transaction.delete_transaction_category',
        name='budget_category'),
    url(r'^transaction/category/?$',
        'simple_budget.views.transaction.transaction.index',
        name='transaction_category'))
