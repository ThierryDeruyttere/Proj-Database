from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from codegalaxy.authentication import require_login, logged_user, authenticate
from codegalaxy.verification import *
from managers.om import *
from managers.cm import challengemanager
import json
from codegalaxy.general import getBrowserLanguage
object_manager = objectmanager.ObjectManager()
challenge_manager = challengemanager.ChallengeManager()

def getAllUsersNames(except_user):
    all_users = object_manager.allUsers()
    all_users_names = []
    for i in all_users:
        if i.id == except_user:
            continue

        name = i.first_name + " " + i.last_name
        img = "/static/" + i.getPicture()
        all_users_names.append({"value": name, "data": img})
    return all_users_names

def prepareDict(lists):
    new_dict = {}
    for i in lists:
        if i.programming_language.name not in new_dict:
            new_dict[i.programming_language.name] = []
        new_dict[i.programming_language.name].append(i.name)

    return new_dict

def getListFromName(list_name, language_code):
    lists = object_manager.getAllExerciseLists(language_code)
    for i in lists:
        if i.name == list_name:
            return i
    return None


@require_login
def challenges(request):
    browser_language = getBrowserLanguage(request)
    user = logged_user(request)
    all_users_names = getAllUsersNames(user.id)
    if request.method == 'POST':
        challenged_name = request.POST.get('challenged')
        challenged = object_manager.getUserByName(challenged_name)
        challenge_type = request.POST.get('challenge_type')
        challenge_list = request.POST.get('possible_lists')
        challenged_list_obj = getListFromName(challenge_list, browser_language.code)

        challenge_manager.createChallenge(user.id, challenged.id, challenge_type, challenged_list_obj.id)

    if request.method == 'GET' and 'available_lists' in request.GET:
        user_pers_lists = user.allPersonalLists()
        #Get all the list objects from the personal lists
        user_lists = [i.exercises_list for i in user_pers_lists]

        challenged = object_manager.getUserByName(request.GET.get('challenged'))
        challenged_pers_lists = challenged.allPersonalLists()
        #Same here
        challenged_lists = [i.exercises_list for i in challenged_pers_lists]

        all_lists = object_manager.getAllExerciseLists(browser_language.id)
        #take an union from all solved lists + lists created by the users
        union = set(user_lists) | set(challenged_lists) | set(user.getAllCreatedLists(browser_language.id)) | set(challenged.getAllCreatedLists(browser_language.id))
        remaining_lists = set(all_lists) - set(union)

        return HttpResponse(json.dumps(prepareDict(remaining_lists)))

    return render(request, 'challenges.html', {"all_users_names": json.dumps(all_users_names),
                                               "user": user
                                                })

def challenge_search(request):
    print("k")