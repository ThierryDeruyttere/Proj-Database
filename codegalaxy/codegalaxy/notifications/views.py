from django.http import HttpResponse
from django.http import HttpResponseRedirect
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

def get_notifications(request):
    user = logged_user(request)
    challenge_requests = challenge_manager.getChallengeRequestsForUser(user.id, 1)
    notifications = {}
    notifications['challenges'] = len(challenge_requests)
    notifications['social'] = len(user.allPendingFriendships()) +  len(user.allPendingGroupMemberships())


    return HttpResponse(json.dumps(notifications))

def handle_request(request):
    print("check")
    user = logged_user(request)
    req_info = request.POST.get('request_info').split('-')

    req_id = req_info[0]
    category = req_info[1]
    print("category: " + category)
    answer = req_info[2]
    print("answer: " + answer)

    if category ==  'friend':
        if answer == 'accept':
            user.confirmFriendship(req_id)
        else:
            user.declineFriendship(req_id)

    if category == 'group':
        if answer == 'accept':
            user.confirmGroupMembership(req_id)
        else:
            user.deleteGroupMembership(req_id)

    return HttpResponse(req_id + "-" + category)
