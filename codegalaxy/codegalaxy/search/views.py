from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.context_processors import request

import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from managers.om import *

object_manager = objectmanager.ObjectManager()

def search(request):
    """
    groups bool
    users bool
    lists bool
    """

    s_term = request.POST.get('term', 'ma')

    s_users = request.POST.get('users', True)
    s_lists = request.POST.get('lists', False)
    s_groups = request.POST.get('groups', False)

    all_users = object_manager.allUsers()
    all_groups = object_manager.allPublicGroups()
    all_lists = object_manager.getAllExerciseLists()

    all_search_obj = []
    if s_users:
        all_search_obj.extend(all_users)
    if s_groups:
        all_search_obj.extend(all_groups)
    if s_lists:
        all_search_obj.extend(all_lists)
        pass

    all_search = {obj: obj.searchString() for obj in all_search_obj}

    results = process.extract(s_term, all_search)

    def getIdentifierForType(obj):
        identifier = ''
        if type(obj) is user.User:
            identifier = 'u'
        elif type(obj) is exerciselist.ExerciseList:
            identifier = 'l'
        elif type(obj) is group.Group:
            identifier = 'g'
        return identifier

    filtered = [[r[2].id, getIdentifierForType(r[2])] for r in results if r[1] >= 50]

    return HttpResponse('<pre>' + str(filtered) + '<pre>')
