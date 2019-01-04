from datetime import datetime
from django import template

register = template.Library()

@register.filter(name='in_the_future')
def in_the_future(date):
    try:
        if datetime.strptime(str(date), '%Y-%m-%d') > datetime.now():
            return True
        else:
            return False
    except ValueError:
        return False

@register.filter(name='currency')
def currency(value):
    if value:
        return "{:,.2f}".format(value)

    return 0.00

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]