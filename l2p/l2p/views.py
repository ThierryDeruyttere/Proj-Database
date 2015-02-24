from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
import hashlib
import sys

import dbw
from om import *

#we'll use one ObjectManager to work with/create the objects stored in the DB
object_manager = objectmanager.ObjectManager()

def home(request):
    return render(request, 'home.html', {})

def user(request, id = 0):
    user = dbw.getUserOnId(id)
    id = int(id)

    if user:
        context = {'user':user}
        if request.session['current_user'] == id:
            context['logged_in'] = True
        return render(request, 'user.html', context)
    else:
        return redirect('/')

def userOverview(request):
    users = dbw.getAll('user')
    return render(request, 'userOverview.html', {'users':users})

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('your_first_name', '')
        last_name = request.POST.get('your_last_name', '')
        email = request.POST.get('your_email', '')
        password = hashlib.md5(request.POST.get('your_password', '').encode('utf-8')).hexdigest()

        try:
            dbw.createNewUser(first_name, last_name, email, password)

        except:
            print("ALREADY A USER WITH THIS EMAIL")
            return render(request, 'register.html', {'error_message': 'This email address is alread in use. Try again.'})
    return render(request, 'register.html', {})

def authenticate(request, email, password):
    #inloggen met email
    user = dbw.getUserOnEmail(email)

    #als het zoeken naar een user met die naam geen lege lijst geeft
    if not user:
        print('There is no user with the name %s' % email)
        return render(request, 'login.html', {})

    if user['password'] == password:
        print("You are getting logged in")
        request.session['current_user'] = user['id']
        return redirect('/me/')
    return render(request, 'login.html', {})

def login(request):
    if 'current_user' not in request.session:
        print('Current_user sessions doesnt exist yet')
        request.session['current_user'] = None
    else:
        print('Already current_user session')

    if request.method == 'POST':
        email = request.POST.get('your_email', '')

        password = hashlib.md5(request.POST.get('your_password', '').encode('utf-8')).hexdigest()
        return authenticate(request, email, password)

    if request.method == 'GET':
        if request.session['current_user']:
            return redirect('/me/')
    return render(request, 'login.html', {})

def logout(request):
    #flush zorgt ervoor dat er geen restjes achterblijven
    #geen idee of dit de juiste manier is
    request.session.flush()
    request.session['current_user'] = None
    return render(request, 'logout.html', {})

def me(request):
    user = dbw.getUserOnId(request.session['current_user'])
    redirect_url = ""
    
    # Switch to /u/<id> if user is logged in, home page otherwise
    if user:
        redirect_url = '/u/{id}'.format(id = request.session['current_user'])
    else:
        redirect_url = '/'
    
    return redirect(redirect_url)

def group(request, id = 0):
    return render(request, 'group.html', {'id':id})

def groupCreate(request, id = 0):
    return render(request, 'groupCreate.html', {})

def list(request, id = 0):
    return render(request, 'list.html', {'id':id})

def question(request, id, question):
    return render(request, 'question.html', {})

def submit(request, id, question):
    return render(request, 'submit.html', {})

def test(request, id = 0):
    user_test = object_manager.createUser(3)
    friends = user_test.allFriends()
    return render(request, 'test.html', {'test': str(user_test),'testfunction': friends })
