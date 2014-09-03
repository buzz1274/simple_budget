from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'simple_budget.views.index', name='index'),)
