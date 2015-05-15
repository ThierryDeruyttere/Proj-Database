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


def prepareChallengeNotif(data):
    d = {}
    for i, val in enumerate(data):
        d[str(i)] = val.challenger.first_name + " " + val.challenger.last_name + " has challenged you for a: " + val.challenge_type.type

    return d

def prepareFriendNotif(request):
    user = logged_user(request)
    friend_requests = {}
    for i, friend_request in enumerate(user.allPendingFriendships2()):
        friend_requests[str(i)] = friend_request.friend.name() + " sent you a friend request."

    return friend_requests

def prepareGroupNotif(request):
    user = logged_user(request)
    group_requests = {}
    for i, group_request in enumerate(user.allPendingGroupMemberships2()):
        group_requests[str(i)] = "You have been invited to join " + group_membership.group.group_name() + "."

    return group_requests

def get_notifications(request):
    user = logged_user(request)
    challenge_requests = challenge_manager.getChallengeRequestsForUser(user.id, 1)
    notifications = {}
    notifications['challenges'] = prepareChallengeNotif(challenge_requests)
    notifications['friend_requests'] = prepareFriendNotif(request)
    notifications['group_requests'] = prepareGroupNotif(request)


    return HttpResponse(json.dumps(notifications))
