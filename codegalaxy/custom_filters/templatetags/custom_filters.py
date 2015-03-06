from django import template

register = template.Library()

@register.filter()
def get_range(number):
    return range(number)