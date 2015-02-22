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

def authenticate(request, username, password):

    #ik doe hier alsof alle users een unieke first_name hebben die als username dient
    user = dbw.getUser(username)

    #als het zoeken naar een user met die naam geen lege lijst geeft
    if not user:
        print('There is no user with the name %s' % username)
        return render(request, 'login.html', {})

    if user[0]['password'] == password:
        request.session['current_user'] = user[0]['id']
        return render(request, 'me.html', {'first_name': user[0]['first_name']})

def login(request):
    if request.method == 'POST':
        request.session['current_user'] = None

        username = request.POST.get('your_name', '')
        password = request.POST.get('your_password', '')

        authenticate(request, username, password)

    if request.method == 'GET':
        if request.session['current_user']:
            user = dbw.getUserInformation(request.session['current_user'])
            return render(request, 'me.html', {'first_name': user[0]['first_name']})
        
    return render(request, 'login.html', {})

def logout(request):
    #flush zorgt ervoor dat er geen restjes achterblijven
    #geen idee of dit de juiste manier is
    request.session.flush()
    request.session['current_user'] = None
    return render(request, 'logout.html', {})

def me(request):
    user = dbw.getUserInformation(request.session['current_user'])
    return render(request, 'me.html', {'first_name': user[0]['first_name']})

def group(request, id = 0):
    return render(request, 'group.html', {'id':id})

def groupCreate(request, id = 0):
    return render(request, 'groupCreate.html', {})

def list(request, id = 0):
    return render(request, 'list.html', {'id':id})

def question(request, id, question):
    return render(request, 'question.html', {})
