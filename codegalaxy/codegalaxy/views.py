from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from collections import OrderedDict
import hashlib
import sys
import re
import time
from random import randint

from codegalaxy.authentication import require_login, logged_user, authenticate
from codegalaxy.verification import *
from managers.om import *
from managers.gm import *
from managers.rm.recommendations import *


# We'll use one ObjectManager to work with/create the objects stored in the DB
object_manager = objectmanager.ObjectManager()
statistics_analyzer = statisticsanalyzer.StatisticsAnalyzer()
# We'll use the graph maker to make pretty graphs with statistical data
graph_manager = graphmanager.GraphManager()

def defaultContext(id):
    profile_picture = "profile_pictures/{}.png".format(id)

    context = {'profile_picture': profile_picture}

    return context

def home(request):
    current_user = logged_user(request)
    friends = []
    recommended_lists = []
    if current_user:
        friends = current_user.allFriends()
        recommended = recommendListsForUser(current_user.id, False, False, True, False, True, False)
        for recommended_list in recommended:
            recommended_lists.append(object_manager.createExerciseList(recommended_list))
    return render(request, 'home.html', {'user': current_user, 'friends': friends, 'recommended': recommended_lists,'random_list': randint(1,object_manager.amountOfLists())})


@require_login
def user(request, id=0):
    current_user = logged_user(request)

    # Make id an int
    id = int(id)
    # Get the user object for that id
    user = object_manager.createUser(id=id)

    if request.method == 'POST':
        if 'add_friend' in request.POST:
            current_user.addFriend(user)

        elif 'confirm_friendship' in request.POST:
            friend_id = request.POST.get('user_id_to_confirm')
            user.confirmFriendship(friend_id)

        elif 'decline_friendship' in request.POST:
            friend_id = request.POST.get('user_id_to_decline')
            user.declineFriendship(friend_id)

        elif 'update_profile' in request.POST:
            f = request.FILES['image']

            destination = open(
                './codegalaxy/static/profile_pictures/' + str(current_user.id) + '.png', 'wb+')

            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

            new_password = hashlib.md5(
            request.POST.get('new_password').encode('utf-8')).hexdigest()
            new_email = request.POST.get('new_email')
            user.updateProfile(new_email, new_password)

    already_friends = False
    if current_user:
        already_friends = current_user.isFriend(user)

    if user:
        friend_list_temp = user.allFriends()
        # names seems too long? -> fix by changing the last part to '...'
        for friend in friend_list_temp:
            if len(friend.last_name) > 12:
                friend.last_name = friend.last_name[:10] + '...'
            if len(friend.first_name) > 12:
                friend.first_name = friend.first_name[:10] + '...'
        # making into a list of lists to facilitate looping/ordering (6
        # friends/row?)
        friend_list = [friend_list_temp[i:i + 4]
                       for i in range(0, len(friend_list_temp), 4)]

        group_list_temp = user.allGroups()
        for group in group_list_temp:
            if len(group.group_name) > 12:
                group.group_name = group.group_name[:10] + '...'
        group_list = [group_list_temp[i:i + 4]
                      for i in range(0, len(group_list_temp), 4)]
        exercise_list = user.allPersonalLists()

        accepted_friendships = sorted(
            user.allFriendships(), key=lambda k: k['datetime'], reverse=True)
        member_of_groups = sorted(
            user.allUserAdded(), key=lambda k: k['datetime'], reverse=True)
        exercises_made = sorted(
            user.allExerciseListsMade(), key=lambda k: k['datetime'], reverse=True)

        all_data = []
        all_data.extend(accepted_friendships)
        all_data.extend(member_of_groups)
        all_data.extend(exercises_made)

        all_data = sorted(all_data, key=lambda k: k['datetime'], reverse=True)

        paginator = Paginator(all_data, 10)  # 10 items per page

        page = request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            # geef de eerste pagina
            data = paginator.page(1)
        except EmptyPage:
            # geen resultaten->laatste page
            data = paginator.page(paginator.num_pages)

        pending_friendships = []
        if current_user.id == user.id:
            pending_friendships = user.allPendingFriendships()


        context = {'user': user, 'group_list': group_list, 'friend_list': friend_list, 'data': data, 'all_data': all_data,
                   'exercise_list': exercise_list, 'already_friends': already_friends, 'pending_friendships': pending_friendships, 'accepted_friendships': accepted_friendships}

        context.update(defaultContext(id))

        if current_user.id == user.id:
            context['my_profile'] = True
            context['old_email'] = user.email
        return render(request, 'user.html', context)

    else:
        return redirect('/')


@require_login
def userOverview(request):
    users = object_manager.allUsers()
    return render(request, 'userOverview.html', {'users': users})


def register(request):
    # Check if we are already logged in
    user = logged_user(request)
    if user:
        return redirect('/u/{id}'.format(id=user.id))

    # There has been a request to register a new user
    if request.method == 'POST':
        first_name = request.POST.get('your_first_name', '')
        last_name = request.POST.get('your_last_name', '')
        email = request.POST.get('your_email', '')

        password = hashlib.md5(
            request.POST.get('your_password').encode('utf-8')).hexdigest()

        gender = request.POST.get('sex')

        try:
            object_manager.insertUser(first_name, last_name, email, password, str(
                time.strftime("%Y-%m-%d")), str(time.strftime("%Y-%m-%d")), gender)
            object_manager.addVerification(
                email, hashlib.md5(email.encode('utf-8')).hexdigest())
            sendVerification(email)

        except:
            return render(request, 'register.html', {'error_register': True})

    return redirect('/')


def login(request):
    if 'current_user' not in request.session:
        request.session['current_user'] = None

    # There has been a request to log in
    if request.method == 'POST':
        error_email = True
        error_password = True

        email = request.POST.get('your_email', '')
        password = hashlib.md5(
            request.POST.get('your_password', '').encode('utf-8')).hexdigest()

        user = authenticate(email, password)

        # Successful login attempt
        if user:
            request.session['current_user'] = user.id
            return redirect('/')
        else:
            return render(request, 'login.html', {'error_login': True, 'your_email': email})

    # We just landed on the login page
    elif request.method == 'GET':
        if logged_user(request):
            return redirect('/me/')

    return render(request, 'login.html', {})


@require_login('/')
def logout(request):
    # flush zorgt ervoor dat er geen restjes achterblijven
    # geen idee of dit de juiste manier is
    request.session.flush()
    request.session['current_user'] = None
    return render(request, 'logout.html', {})


@require_login
def me(request):
    user_url = '/u/{id}'.format(id=logged_user(request).id)
    return redirect(user_url)


@require_login
def group(request, id=0):
    # https://cdn4.iconfinder.com/data/icons/e-commerce-icon-set/48/More-512.png

    # https://cdn2.iconfinder.com/data/icons/picol-vector/32/group_half-512.png
    # https://cdn2.iconfinder.com/data/icons/picol-vector/32/group_half_add-512.png

    user = logged_user(request)

    group = object_manager.createGroup(id)

    if request.method == 'POST':
        if 'become_member' in request.POST:
            group.insertMember(user.id, 0, str(time.strftime("%Y-%m-%d")))

        elif 'add_friend' in request.POST:
            friend_id = request.POST.get('user_id_to_add', '')
            group.insertMember(friend_id, 0, str(time.strftime("%Y-%m-%d")))

    is_member = False
    if group:

        user_list = group.allMembers()

        if group.group_type == 1:
            # Only users in this group can access this page
            correct_user = False
            for u in user_list:
                if u.id == user.id:
                    correct_user = True

            if not correct_user:
                return redirect('/')

        try:
            group_size = len(user_list)

        except:
            group_size = 0

        if group_size > 0:
            for x in range(0, group_size):
                if user.email == user_list[x].email:
                    is_member = True

        accepted_friendships = []
        member_of_groups = []
        exercises_made = []
        all_data = []

        if group_size > 0:
            for one_user in user_list:
                accepted_friendships = one_user.allFriendships()
                member_of_groups = one_user.allUserAdded()
                exercises_made = one_user.allExerciseListsMade()

                all_data.extend(accepted_friendships)
                all_data.extend(member_of_groups)
                all_data.extend(exercises_made)

            all_data = sorted(
                all_data, key=lambda k: k['datetime'], reverse=True)

        paginator = Paginator(all_data, 15)  # 10 items per page

        page = request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            # geef de eerste pagina
            data = paginator.page(1)
        except EmptyPage:
            # geen resultaten->laatste page
            data = paginator.page(paginator.num_pages)

        currentuser_friend_list = user.allFriendsNotMemberOfGroupWithID(id)

        remaining_friends = []
        for friend in currentuser_friend_list:
            inList = False
            for user in user_list:
                if friend.id == user.id:
                    inList = True

            if not inList:
                remaining_friends.append(friend)

        context = {'user': user, 'data': data, 'all_data': all_data, 'id': id, 'group': group, 'user_list':
                   user_list, 'group_size': group_size, 'currentuser_friend_list': remaining_friends, 'is_member': is_member}
        return render(request, 'group.html', context)

    else:
        return redirect('/')


@require_login
def groupOverview(request):
    # Biggest Groups
    biggest_groups = statistics_analyzer.biggestGroupsTopX(5)
    color_info1 = graphmanager.ColorInfo(
        "#F7464A", "#F7464A", "#FF5A5E", "#FF5A5E")
    color_info2 = graphmanager.ColorInfo(
        "#46BFBD", "#46BFBD", "#5AD3D1", "#46BFBD")
    bar_chart = graph_manager.makeBarChart('groups', 270, 180, [
                                           color_info2, color_info1], biggest_groups['labels'], biggest_groups['data'], "#members")

    # https://cdn2.iconfinder.com/data/icons/picol-vector/32/group_half-512.png
    # https://cdn2.iconfinder.com/data/icons/picol-vector/32/group_half_add-512.png
    group_list_temp = object_manager.allPublicGroups()
    for group in group_list_temp:
        if len(group.group_name) > 12:
            group.group_name = group.group_name[:10] + '...'

    groups = [group_list_temp[i:i + 4]
              for i in range(0, len(group_list_temp), 4)]

    if groups:
        return render(request, 'groupOverview.html', {'groups': groups, 'biggest_groups': bar_chart})
    # else:
        # return redirect('/')
    return redirect('/g/create')


@require_login
def groupCreate(request, id=0):
    user = logged_user(request)
    if request.method == 'POST':
        group_name = request.POST.get('group_name', '')

        # !!!!!!
        # iemand een idee hoe ik uit een switch een waarde haal?
        group_type = request.POST.get('group_type')
        try:
            if group_type == 'on':
                object_manager.insertGroup(
                    group_name, 1, str(time.strftime("%Y-%m-%d")))
            else:
                object_manager.insertGroup(
                    group_name, 0, str(time.strftime("%Y-%m-%d")))

            # auto add user when making a private group?

            group = object_manager.createGroupOnName(group_name)
            group.insertMember(user.id, 2, str(time.strftime("%Y-%m-%d")))
            return redirect('/g/' + str(group.id))

        except:
            return render(request, 'groupCreate.html', {'error_group_name': 'This name is already in use. Please try again...'})

    return render(request, 'groupCreate.html', {})


def list(request, id=0):
    return render(request, 'list.html', {'id': id})


@require_login
def submit(request, id, question):
    return render(request, 'submit.html', {})


def verify(request, hash_seq):
    if object_manager.needsVerification(hash_seq):
        email = object_manager.acceptVerification(hash_seq)
        sendVerificationAccepted(email)
        return render(request, 'verify.html', {})

    return redirect('/')


def test(request, id=0):
    # Quick tests/changes
    exercise_test = object_manager.createExercise(1, 'en')
    exercise_test2 = object_manager.createExercise(1, 'en')
    # exercise_test.difficulty = 9001
    new_answers = ["a", "b", "c"]
    new_hints = ["hint1", "hint2"]
    #exercise_test.update(2, new_answers, new_hints)

    # test
    user_test = object_manager.createUser(id=1)
    # UPDATE USER test
    user_test.first_name = "testerino"
    user_test.last_name = "thafuk"
    user_test.password = "peswert"
    user_test.permissions = 1
    user_test.email = "lol@test.fk"
    user_test.joined_on = "2-2-2"
    user_test.last_login = str(time.strftime("%Y-%m-%d"))
    user_test.gender = "F"
    user_test.save()
    # testfunction
    friends = user_test.allFriends()
    # testfunction2
    groups = user_test.allGroups()
    # testfunction 3
    lists = user_test.allPersonalLists()
    # testfunction4
    permission = user_test.checkPermission(1)
    # testfunction5
    personalexercises = []
    for list_ in lists:
        personalexercises += list_.allExercises("en")
    # testfunction6
    #exercise_test = object_manager.createExercise(1, 'en')
    # testfunction7
    hints = exercise_test.allHints()
    # testfunction8
    answers = exercise_test.allAnswers()
    # testfunction9
    # TODO 31 ns testen
    group_test = object_manager.createGroup(1)
    group_test.group_name = "Testgroup"
    group_test.group_type = 5
    group_test.created_on = str(time.strftime("%Y-%m-%d"))
    group_test.save()
    # testfunction10
    exercise_list_test = object_manager.createExerciseList(1)
    #exercise_list_test.name = "testlist"
    #exercise_list_test.difficulty = 4
    #exercise_list_test.description = "no"
    #exercise_list_test.programming_language = 2
    #reference test -> copying multiple times???
    exercise_list_test.insertExerciseByReference(1)
    exercise_list_test.insertExerciseByReference(2)
    #new_id = exercise_list_test.unreferenceExercise(3)
    #exercise_test3 = object_manager.createExercise(new_id,'en')

    # testfunction11
    subjects = exercise_list_test.allSubjects()
    # testfunction12
    exercises = exercise_list_test.allExercises('en')
    print("before")
    for ex in exercises:
        print(ex)
        print("\n")
    exercise_list_test.reorderExercises([3,2,4,1],'en')
    exercises = exercise_list_test.allExercises('en')
    print("remade")
    for ex in exercises:
        print(ex)
        print("\n")
    #exercises[2].penalty = 3
    #exercises[2].save()
    # testfunction13
    members = group_test.allMembers()

    return render(request, 'test.html', {'test': str(user_test), 'testfunction': ' '.join([str(friend) for friend in friends]), 'testfunction2': ' '.join([str(group) for group in groups]), 'testfunction3': ' '.join([str(list_) for list_ in lists]), 'testfunction4': permission, 'testfunction5': ' '.join([str(ex) for ex in personalexercises]), 'testfunction6': str(exercise_test), 'testfunction7': hints, 'testfunction8': answers, 'testfunction9': 'Group: ' + str(group_test), 'testfunction10': 'List: ' + str(exercise_list_test), 'testfunction11': subjects, 'testfunction12': ' '.join([str(exercise) for exercise in exercises]), 'testfunction13': ' '.join([str(member) for member in members])})

def tables(request):
    import dbw
    if request.method == 'GET':
        table = request.GET.get('sql_table', '')
        if table != '':
            data = dbw.getAll(table)
            return render(request, 'tables.html', {'data': data, 'keys': data[0].keys()})
    return render(request, 'tables.html', {})

def python(request):
    return render(request, 'python.html', {})


def recommendations(request):
    user_test = object_manager.createUser(id=1)
    lists = user_test.allPersonalLists()
    b = recommendListsForUser(1)
    recommended = recommendNextExerciseLists(lists[0], 2)
    return render(request, 'recommendations.html', {'test': str(b), 'test2': str(recommended)})


def graphs(request):
    # LINE CHART
    # color_info = graphmanager.ColorInfo()
    # test_line_graph = graph_manager.makeLineChart('Buyers',600,400,color_info
    # ,["January","February","March","April","May","June"]
    # ,[203,156,99,251,305,247])

    # PIE CHART
    stats = statistics_analyzer.AmountOfExerciseListsPerProgrammingLanguage()
    test_pie_graph = graph_manager.makePieChart(
        'colours', 600, 400, graphmanager.color_tuples, stats['labels'], stats['data'])

    # BARCHART
    stats = statistics_analyzer.biggestGroupsTopX(5)
    color_info1 = graphmanager.ColorInfo(
        "rgba(151,187,205,0.5)", "rgba(151,187,205,0.8)", "rgba(151,187,205,0.75)", "rgba(151,187,205,1)")
    color_info2 = graphmanager.ColorInfo(
        "rgba(220,220,220,0.5)", "rgba(220,220,220,0.8)", "rgba(220,220,220,0.75)", "rgba(220,220,220,1)")
    test_bar_graph = graph_manager.makeBarChart(
        'kek', 600, 400, [color_info2, color_info1], stats['labels'], stats['data'], "#members")

    # BARCHART 2
    stats = statistics_analyzer.mostExerciseListsTopX(5)
    test_bar_graph2 = graph_manager.makeBarChart('kek2', 600, 400, [
                                                 color_info2, color_info1], stats['labels'], stats['data'], ["#exercises"])

    # BARCHART 3
    stats = statistics_analyzer.compareUserExercisesPerProgrammingLanguageWithFriend(
        1, 2)
    test_bar_graph3 = graph_manager.makeBarChart('kek3', 600, 400, [
                                                 color_info2, color_info1], stats['labels'], stats['data'], ["user", "friend"])

    # BARCHART 3
    stats = statistics_analyzer.mostPopularSubjectsTopX(1)
    test_bar_graph4 = graph_manager.makeBarChart('kek4', 600, 400, [
                                                 color_info2, color_info1], stats['labels'], stats['data'], ["subject"])

    # BARCHART 4
    stats = statistics_analyzer.listScoreSpread(1)
    test_bar_graph5 = graph_manager.makeBarChart(
        'kek5', 600, 400, [color_info2, color_info1], stats['labels'], stats['data'], ["score"])

    return render(request, 'graphs.html', {'teststr': test_bar_graph2,
                                           'teststr2': test_pie_graph,
                                           'teststr3': test_bar_graph,
                                           'teststr4': test_bar_graph3,
                                           'teststr5': test_bar_graph4,
                                           'teststr6': test_bar_graph5})
