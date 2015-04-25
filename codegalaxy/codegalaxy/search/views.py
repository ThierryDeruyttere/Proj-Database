from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.context_processors import request

from codegalaxy.search import *

from codegalaxy.authentication import require_login, logged_user

def social(request):
    s_term = request.POST.get('term', '')

    s_my_groups = bool(request.POST.get('my_groups', 'false') != 'false')

    results = search(s_term, s_users=(not s_my_groups), s_groups=True)

    current_user = logged_user(request)
    if current_user and s_my_groups:
        results = [result for result in results if result.id in [g.id for g in current_user.allGroups()]]

    response = ''
    for result in results:

        t = 'u'
        if type(result) is group.Group:
            t = 'g'

        group_owner = ""
        friends_in_group = " | "
        for friend in current_user.allFriends():
            for member in result.allMembers():
                if result.getUserPermissions(member.id) == 0:
                    group_owner = member.name()
                if friend.id == member.id:
                    friends_in_group += friend.name() + " | "

        response += '''
        <div class="large-12 columns end">
          <div class="panel radius">
            <div class="row">
              <div class="large-3 columns">
                <a href="/{type}/{id}">
                  <img src="/static/{picture}" />
                </a>
              </div>
              <div class="large-9 columns left">
                <div class="row">
                  <a href="/{type}/{id}">
                    <h5 class="text-cut-off"><b>{name}</b> ({nr_of_members} members)</h5>
                  </a>
                </div>
                <br>
                <div class="row">
                  <a href="/{type}/{id}">
                    <h6 class="text-cut-off"><b>Owner:</b> {owner}</h6>
                  </a>
                </div>
                <div class="row">
                  <a href="/{type}/{id}">
                    <h6><b>Friends in group:</b> {friends_in_this_group}</h6>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        '''.format(type=t, id=result.id, picture=result.getPicture(), nr_of_members = len(result.allMembers()), name=result.name(), owner=group_owner, friends_in_this_group=friends_in_group)

    return HttpResponse(response)
