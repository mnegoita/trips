from django import template
from django.utils.safestring import mark_safe

register = template.Library()




@register.filter()
def floor_div(value, arg):
    try:
        return int(value) // int(arg)
    except (ValueError, ZeroDivisionError):
        return None
    
 
@register.filter()
def modulo(value, arg):
    try:
        return value % arg 
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name

@register.filter()
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural


@register.filter()
def placeholder(value):
    """
    Render a muted placeholder if value equates to False.
    """
    if value:
        return value
    placeholder = '<span class="text-muted">&mdash;</span>'
    return mark_safe(placeholder)


