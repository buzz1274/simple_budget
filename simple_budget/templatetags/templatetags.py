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