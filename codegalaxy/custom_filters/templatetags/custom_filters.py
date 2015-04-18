from django import template
from codegalaxy import authentication
from managers.om import objectmanager
from django.template import resolve_variable
from django import template
from django.template import Library, Node
from copy import deepcopy

register = template.Library()

@register.filter()
def get_range(number):
    return range(number)

@register.assignment_tag(takes_context=True)
def getProfilePicture(context):
    object_manager = objectmanager.ObjectManager()
    return authentication.logged_user(context['request']).getPicture()

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


@register.filter
def copy_list(l):
    return deepcopy(l)