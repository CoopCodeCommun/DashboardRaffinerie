# mon_application/templatetags/my_filters.py
from django import template

register = template.Library()

@register.filter(name='zip_lists')
def zip_lists(a, b):
    return zip(a, b)

@register.filter()
def verbose_name(field, model):
     # Va chercher le nom "verbeux" du champ associé au modèle
    return model._meta.get_field(field).verbose_name

@register.filter()
def is_editable(field, model):
    return model._meta.get_field(field).editable


@register.filter
def is_int(value):
    return isinstance(value, int)

@register.filter
def is_bool(value):
    return isinstance(value, bool)

@register.filter
def is_char(value):
    return isinstance(value, str)
