from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from codegalaxy.authentication import require_login, logged_user, authenticate
from codegalaxy.verification import *
from managers.om import *
from codegalaxy.general import getBrowserLanguage

object_manager = objectmanager.ObjectManager()


def getAllUsersNames():
    all_users = object_manager.allUsers()
    all_users_names = []
    for i in all_users:
        all_users_names.append(i.first_name + " " + i.last_name)
    return all_users_names

@require_login
def challenges(request):
    user = logged_user(request)
    all_users_names = getAllUsersNames()


    return render(request, 'challenges.html', {"all_users_names": all_users_names
                                                })