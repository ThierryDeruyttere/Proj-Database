from django import template
from codegalaxy import authentication

register = template.Library()

@register.filter()
def get_range(number):
    return range(number)

@register.assignment_tag(takes_context=True)
def check_loggedIn(context):
    try:
        print("checking")
        if authentication.logged_user(context['request']) is None:
            print("false")
            return False
        print("true")
        return True
    except Exception as e:
        return False