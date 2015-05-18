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
    notifications['social'] = len(user.allPendingFriendships2()) +  len(user.allPendingGroupMemberships2())


    return HttpResponse(json.dumps(notifications))

def handle_request(request):
    

    return
