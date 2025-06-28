# templatetags/cart_tag.py

from django import template
register = template.Library()

@register.filter
def multiply(value, arg):
    return int(value) * int(arg)
