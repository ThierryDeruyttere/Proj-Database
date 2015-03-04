from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

import hashlib
import sys
import re

from codegalaxy.authentication import require_login, logged_user, authenticate
from managers.om import *
from managers.gm import *

# We'll use one ObjectManager to work with/create the objects stored in the DB
object_manager = objectmanager.ObjectManager()

def home(request):
    return render(request, 'home.html', {})

@require_login
def user(request, id = 0):
    current_user = logged_user(request)

    # Make id an int
    id = int(id)
    # Get the user object for that id
    user = object_manager.createUser(id = id)

    if request.method == 'POST':
        current_user.addFriend(user)

    already_friends = False
    if current_user:
        #already_friends = current_user.isFriend(user)
        pass

    if user:
        friend_list = user.allFriends()

        group_list = user.allGroups()
        exercise_list = user.allPersonalLists()
        context = {'user':user, 'group_list':group_list, 'friend_list': friend_list, 'exercise_list':exercise_list, 'already_friends': already_friends}

        if request.session['current_user'] == id:
            context['logged_in'] = True
        return render(request, 'user.html', context)
    else:
        return redirect('/')

@require_login
def userOverview(request):
    users = object_manager.allUsers()
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

        password = hashlib.md5(request.POST.get('your_password').encode('utf-8')).hexdigest()

        if not password:
            error_password = True

        try:
            object_manager.insertUser(first_name, last_name, email, password)
        except:
            return render(request, 'register.html', {'error_message': 'This email address is alread in use.'})

    return render(request, 'register.html', {})

def login(request):
    if 'current_user' not in request.session:
        request.session['current_user'] = None

    # There has been a request to log in
    if request.method == 'POST':
        error_email = True
        error_password = True

        email = request.POST.get('your_email', '')
        password = hashlib.md5(request.POST.get('your_password', '').encode('utf-8')).hexdigest()

        user = authenticate(email, password)

        # Successful login attempt
        if user:
            request.session['current_user'] = user.id
            return redirect('/me/')
        else:
            return render(request, 'login.html', {'error_login': True, 'your_email': email})

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

@require_login
def group(request, id = 0):
    #https://cdn4.iconfinder.com/data/icons/e-commerce-icon-set/48/More-512.png

    #https://cdn2.iconfinder.com/data/icons/picol-vector/32/group_half-512.png
    #https://cdn2.iconfinder.com/data/icons/picol-vector/32/group_half_add-512.png

    user = logged_user(request)

    group = object_manager.createGroup(id)

    if request.method == 'POST':
        group.insertMember(user.id, id)

    is_member = False
    if group:
        user_list = group.allMembers()


        try:
            group_size = len(user_list)

        except:
            group_size = 0

        if group_size > 0:
            for x in range(0, group_size):
                if user.email == user_list[x].email:
                    is_member = True

        return render(request, 'group.html', {'id':id, 'group': group, 'user_list': user_list, 'group_size': group_size, 'is_member': is_member})

    else:
        return redirect('/')

@require_login
def groupOverview(request):
    #https://cdn2.iconfinder.com/data/icons/picol-vector/32/group_half-512.png
    #https://cdn2.iconfinder.com/data/icons/picol-vector/32/group_half_add-512.png
    groups = object_manager.allGroups()

    if groups:
        return render(request, 'groupOverview.html', {'groups': groups})
    #else:
        #return redirect('/')
    return redirect('/g/create')

@require_login
def groupCreate(request, id = 0):

    if request.method == 'POST':
        group_name = request.POST.get('group_name', '')

        #!!!!!!
        #iemand een idee hoe ik uit een switch een waarde haal?
        group_type = 0

        try:
            object_manager.insertGroup(group_name, group_type)
            return redirect('/g/overview')
        except:
            return render(request, 'groupCreate.html', {'error_group_name': 'This name is already in use. Please try again...'})

    return render(request, 'groupCreate.html', {})

def list(request, id = 0):
    return render(request, 'list.html', {'id':id})

@require_login
def submit(request, id, question):
    return render(request, 'submit.html', {})

def test(request, id = 0):
    # Quick tests/changes
    exercise_test = object_manager.createExercise(1,'en')
    exercise_test2 = object_manager.createExercise(1,'en')
    #exercise_test.difficulty = 9001
    new_answers = ["a","b","c"]
    new_hints = ["hint1","hint2"]
    exercise_test.update(2,new_answers,new_hints)
    print(exercise_test)

    # test
    user_test = object_manager.createUser(id=1)
    # UPDATE USER test
    user_test.first_name = "testerino"
    user_test.last_name = "thafuk"
    user_test.password = "peswert"
    user_test.permissions = 1
    user_test.email = "lol@test.fk"
    user_test.save()
    #testfunction
    friends = user_test.allFriends()
    #testfunction2
    groups = user_test.allGroups()
    #testfunction 3
    lists = user_test.allPersonalLists()
    #testfunction4
    permission = user_test.checkPermission(1)
    #testfunction5
    personalexercises = []
    for list_ in lists:
        personalexercises += list_.allExercises("en")
    #testfunction6
    exercise_test = object_manager.createExercise(1,'en')
    #testfunction7
    hints = exercise_test.allHints()
    #testfunction8
    answers = exercise_test.allAnswers()
    #testfunction9
    group_test = object_manager.createGroup(1)
    group_test.group_name = "Testgroup"
    group_test.group_type = 5
    group_test.save()
    #testfunction10
    exercise_list_test = object_manager.createExerciseList(1)
    exercise_list_test.name = "testlist"
    exercise_list_test.difficulty = 4
    exercise_list_test.description = "no"
    exercise_list_test.programming_language = 2
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


def graphs(request):
    #We'll use the graph maker to make pretty graphs with statistical data
    graph_manager = graphmanager.GraphManager()

    # LINE CHART
    color_info = graphmanager.ColorInfo()
    test_line_graph = graph_manager.makeLineChart('Buyers',600,400,color_info
    ,["January","February","March","April","May","June"]
    ,[203,156,99,251,305,247])

    #PIE CHART
    all_prog_languages = object_manager.allProgrammingLanguages()
    languages = []
    amount_of_exercises = []
    for prog_lang in all_prog_languages:
        count = object_manager.countExerciseListsForProgrammingLanguageID(prog_lang['id'])
        languages.append(prog_lang['name'])
        amount_of_exercises.append(count['amount'])
    test_pie_graph = graph_manager.makePieChart('colours',600,400,graphmanager.color_tuples,languages,amount_of_exercises)

    #BARCHART
    color_info1 = graphmanager.ColorInfo("rgba(151,187,205,0.5)","rgba(151,187,205,0.8)","rgba(151,187,205,0.75)","rgba(151,187,205,1)")
    color_info2 = graphmanager.ColorInfo("rgba(220,220,220,0.5)","rgba(220,220,220,0.8)","rgba(220,220,220,0.75)","rgba(220,220,220,1)")
    test_bar_graph = graph_manager.makeBarChart('kek',600,400,[color_info2,color_info1],["January","February","March","April","May","June"],[[456,479,324,569,702,600],[364,504,605,400,345,320]])

    return render(request, 'graphs.html',{'teststr': test_line_graph,'teststr2' : test_pie_graph,'teststr3' : test_bar_graph})
