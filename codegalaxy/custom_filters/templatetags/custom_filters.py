from django import template
from codegalaxy import authentication

register = template.Library()

@register.filter()
def get_range(number):
    return range(number)

@register.assignment_tag(takes_context=True)
def check_loggedIn(context):
    try:
        if authentication.logged_user(context['request']) is None:
            return False
        return True
    except Exception as e:
        return False

@register.filter
def for_key(d, key):
    return d.get(key)