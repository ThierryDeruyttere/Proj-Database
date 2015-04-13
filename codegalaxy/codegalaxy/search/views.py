from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.context_processors import request

from codegalaxy.search import *


def groupOverview(request):
    s_term = request.POST.get('term', '')

    results = search(s_term, s_groups=True)

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
        '''.format(id=result.id, picture=result.getGroupPicture(), name=result.group_name)

    return HttpResponse(response)
