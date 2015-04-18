from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.context_processors import request

from codegalaxy.search import *

from codegalaxy.authentication import require_login, logged_user

def groupOverview(request):
    s_term = request.POST.get('term', '')
    s_my_groups = bool(request.POST.get('my_groups', 'false') != 'false')

    results = search(s_term, s_users=(not s_my_groups), s_groups=True)

    current_user = logged_user(request)
    if current_user and s_my_groups:
        results = [result for result in results if result.id in [g.id for g in current_user.allGroups()]]

    response = ''
    for result in results:
        response += '''
        <div class="large-3 columns end">
          <div class="panel radius">
            <a href="/g/{id}">
              <img src="/static/{picture}" />
              <div>
                <h6 class="text-cut-off">{name}</h6>
              </div>
            </a>
          </div>
        </div>
        '''.format(id=result.id, picture=result.getGroupPicture(), name=result.name())

    return HttpResponse(response)
