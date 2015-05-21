from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.context_processors import request
from django.utils.translation import ugettext as _

from codegalaxy.search import *

from codegalaxy.authentication import require_login, logged_user
from managers.om import *

import time
from datetime import datetime

def social(request):
    s_term = request.POST.get('term', '')

    s_my_groups = bool(request.POST.get('my_groups', 'false') != 'false')

    results = search(s_term, s_users=(not s_my_groups), s_groups=True)

    current_user = logged_user(request)
    if current_user and s_my_groups:
        results = [result for result in results if result.id in [g.id for g in current_user.allGroups()]]

    response = ''
    for result in results:
        response += result.searchResult(current_user)

    if response == '':
        response = _('There are no search results to display.')

    return HttpResponse(response)

def badge(request):
    user = logged_user(request)
    new_badge = request.POST.get('badge_name', '')
    user.changeBadge(new_badge)
    return HttpResponse(new_badge)

def addmembers(request):
    object_manager = objectmanager.ObjectManager()

    s_term = request.POST.get('term', '')
    group_id = request.POST.get('group_id', '')

    current_user = logged_user(request)
    group = object_manager.createGroup(group_id)

    results = searchUser(s_term, group)

    response = ''
    for result in results:
        print("We gaan is beginnen voor elk resultaat")
        response += result.searchGroupResult(current_user, group.id)

    if response == '':
        response = _('There are no search results to display.')

    return HttpResponse(response)

def invitemember(request):
    print("TITS OR GTFO")
    object_manager = objectmanager.ObjectManager()

    group_id = request.POST.get('group_id', '')
    friend_id = request.POST.get('user_id', '')
    print(group_id)
    print(friend_id)
    group = object_manager.createGroup(group_id)
    print(group.name())
    print(group.id)
    group.insertMember(friend_id, 2, str(time.strftime("%Y-%m-%d %H:%M:%S")),"Pending")
    return HttpResponse()

