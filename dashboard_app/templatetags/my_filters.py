# mon_application/templatetags/my_filters.py
from django import template

register = template.Library()

@register.filter(name='zip_lists')
def zip_lists(a, b):
    return zip(a, b)