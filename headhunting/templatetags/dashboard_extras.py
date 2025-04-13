from django import template

register = template.Library()

@register.filter(name='div')
def div(value, arg):
    """除法过滤器"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter(name='mul')
def mul(value, arg):
    """乘法过滤器"""
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0 