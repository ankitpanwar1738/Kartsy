from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except:
        return 0

@register.filter
def gt(value, arg):
    try:
        return float(value) > float(arg)
    except:
        return False
