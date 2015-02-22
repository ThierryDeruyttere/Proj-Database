from django.http import HttpResponse
from django.shortcuts import render

import dbw
from om import *

#we'll use one ObjectManager to work with/create the objects stored in the DB
object_manager = objectmanager.ObjectManager()

def home(request):
    return render(request, 'home.html', {})

def user(request, id = 0):
    return render(request, 'user.html', {'id':id})

def userOverview(request):
    users = dbw.getAll('user')
    return render(request, 'userOverview.html', {'users':users})

def login(request):
    return render(request, 'login.html', {})

def group(request, id = 0):
    return render(request, 'group.html', {'id':id})

def groupCreate(request, id = 0):
    return render(request, 'groupCreate.html', {})

def list(request, id = 0):
    return render(request, 'list.html', {'id':id})

def question(request, id, question):
    return render(request, 'question.html', {})
