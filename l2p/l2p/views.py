from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

import hashlib
import sys

from om import *
from l2p.authentication import require_login, logged_user, authenticate

# We'll use one ObjectManager to work with/create the objects stored in the DB
object_manager = objectmanager.ObjectManager()

def home(request):
    return render(request, 'home.html', {})

def user(request, id = 0):
    # Make id an int
    id = int(id)
    # Get the user object for that id
    user = object_manager.createUser(id = id)

    if user:
        context = {'user':user}
        if request.session['current_user'] == id:
            context['logged_in'] = True
        return render(request, 'user.html', context)
    else:
        return redirect('/')

def userOverview(request):
    import dbw
    users = dbw.getAll('user')
    return render(request, 'userOverview.html', {'users':users})

def register(request):
    user = logged_user(request)

    if user:
        return redirect('/u/{id}'.format(id = user.id))
    # There has been a request to register a new user

    if request.method == 'POST':
        first_name = request.POST.get('your_first_name', '')
        last_name = request.POST.get('your_last_name', '')
        email = request.POST.get('your_email', '')
        password = hashlib.md5(request.POST.get('your_password', '').encode('utf-8')).hexdigest()

        try:
            object_manager.insertUser(first_name, last_name, email, password)

        except:
            return render(request, 'register.html', {'error_message': 'This email address is alread in use. Try again.'})

    return render(request, 'register.html', {})

def login(request):
    if 'current_user' not in request.session:
        request.session['current_user'] = None

    # There has been a request to log in
    if request.method == 'POST':
        email = request.POST.get('your_email', '')
        password = hashlib.md5(request.POST.get('your_password', '').encode('utf-8')).hexdigest()

        user = authenticate(email, password)

        # Successful login attempt
        if user:
            request.session['current_user'] = user.id
            return redirect('/me/')

    # We just landed on the login page
    elif request.method == 'GET':
        if logged_user(request):
            return redirect('/me/')

    return render(request, 'login.html', {})

@require_login('/')
def logout(request):
    #flush zorgt ervoor dat er geen restjes achterblijven
    #geen idee of dit de juiste manier is
    request.session.flush()
    request.session['current_user'] = None
    return render(request, 'logout.html', {})

@require_login
def me(request):
    user_url = '/u/{id}'.format(id = logged_user(request).id)
    return redirect(user_url)

def group(request, id = 0):
    return render(request, 'group.html', {'id':id})

@require_login
def groupCreate(request, id = 0):
    return render(request, 'groupCreate.html', {})

def list(request, id = 0):
    return render(request, 'list.html', {'id':id})

@require_login
def question(request, id, question):
    return render(request, 'question.html', {})

@require_login
def submit(request, id, question):
    return render(request, 'submit.html', {})

def test(request, id = 0):
    # test
    user_test = object_manager.createUser(id=1)
    #testfunction
    friends = user_test.allFriends()
    #testfunction2
    groups = user_test.allGroups()
    #testfunction 3
    lists = user_test.allPersonalLists()
    #testfunction4
    permission = user_test.checkPermission(1)
    #testfunction5
    #TODO fix this test by adding stuff to DB?
    personalexercises = []
    for list_ in lists:
        #TODO uncomment this when everything is k
        personalexercises = []
        #personalexercises += list_.allExercises()
    #testfunction6
    exercise_test = object_manager.createExercise(1,'en')
    #testfunction7
    hints = exercise_test.allHints()
    #testfunction8
    answers = exercise_test.allAnswers()
    #testfunction9
    group_test = object_manager.createGroup(1)
    #testfunction10
    exercise_list_test = object_manager.createExerciseList(1)
    #testfunction11
    subjects = exercise_list_test.allSubjects()
    #testfunction12
    exercises = exercise_list_test.allExercises('en')
    #testfunction13
    members = group_test.allMembers()

    return render(request, 'test.html', {'test': str(user_test),'testfunction': ' '.join([str(friend) for friend in friends])
    ,'testfunction2': ' '.join([str(group) for group in groups]),'testfunction3': ' '.join([str(list_) for list_ in lists])
    ,'testfunction4': permission,'testfunction5': ' '.join([str(ex) for ex in personalexercises])
    ,'testfunction6': str(exercise_test),'testfunction7': hints,'testfunction8': answers
    ,'testfunction9': 'Group: '+str(group_test),'testfunction10': 'List: '+str(exercise_list_test)
    ,'testfunction11': subjects,'testfunction12': ' '.join([str(exercise) for exercise in exercises])
    ,'testfunction13': ' '.join([str(member) for member in members])})

def tables(request):
    import dbw
    if request.method == 'GET':
        table = request.GET.get('sql_table', '')
        if(table != ''):
            data = dbw.getAll(table)
            return render(request, 'tables.html',{'data' : data, 'keys' : data[0].keys()})

    return render(request, 'tables.html',{})

def python(request):
    return render(request, 'python.html', {})
