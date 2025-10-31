from django import template

register = template.Library()

@register.filter
def absoluteValue(value):
    try:
        if value < 0:
            return -(value)
        else:
            return value
    except:
        return value