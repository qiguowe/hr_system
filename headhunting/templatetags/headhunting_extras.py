from django import template

register = template.Library()

@register.filter
def endswith(value, arg):
    """检查字符串是否以指定后缀结尾"""
    return value.endswith(arg) 