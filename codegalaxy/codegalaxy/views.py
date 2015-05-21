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
from codegalaxy.general import getBrowserLanguage

import os.path
from PIL import Image

# We'll use one ObjectManager to work with/create the objects stored in the DB
object_manager = objectmanager.ObjectManager()
statistics_analyzer = statisticsanalyzer.StatisticsAnalyzer()
# We'll use the graph maker to make pretty graphs with statistical data
graph_manager = graphmanager.GraphManager()

def home(request):
    current_user = logged_user(request)
    friends = []
    recommended_lists = []
    feed = []
    browser_lang = getBrowserLanguage(request)
    if current_user:
        current_user_accepted_friendships = current_user.allFriendsWith()
        current_user_member_of_groups = current_user.allGroupsJoined()
        current_user_exercises_made = current_user.allExerciseListsShared(browser_lang.id)
        current_user_exercises_created = current_user.getAllExercisesCreated(browser_lang.id)

        for userInGroup in current_user_member_of_groups:
                if userInGroup.group.group_type == 1:
                    current_user_member_of_groups.remove(userInGroup)

        feed.extend(current_user_member_of_groups)
        feed.extend(current_user_exercises_made)
        feed.extend(current_user_exercises_created)

        for friendship in current_user_accepted_friendships:
            friend = object_manager.createUser(id=friendship.friend.id)

            accepted_friendships = friend.allFriendsWith()
            member_of_groups = friend.allGroupsJoined()
            exercises_made = friend.allExerciseListsShared(browser_lang.id)
            exercises_created = friend.getAllExercisesCreated(browser_lang.id)

            for memberInGroup in member_of_groups:
                if memberInGroup.group.group_type == 1:
                    member_of_groups.remove(memberInGroup)

            feed.extend(accepted_friendships)
            feed.extend(member_of_groups)
            feed.extend(exercises_made)
            feed.extend(exercises_created)

        feed = sorted(feed, key=lambda k: k.datetime, reverse=True)

        paginator = Paginator(feed, 10)  # 10 items per page

        page = request.GET.get('page')
        try:
            feed_data = paginator.page(page)
        except PageNotAnInteger:
            # geef de eerste pagina
            feed_data = paginator.page(1)
        except EmptyPage:
            # geen resultaten->laatste page
            feed_data = paginator.page(paginator.num_pages)

        recommended = recommendListsForUser(
            current_user, True, True, True, True, True, False)
        for recommended_list in recommended:
            recommended_lists.append(
                object_manager.createExerciseList(recommended_list, browser_lang.id))

        return render(request, 'home.html', {'user': current_user, 'feed_data': feed_data, 'feed': feed, 'friends': friends,
                'recommended': recommended_lists, 'random_list': imFeelingLucky(current_user)})
    return render(request, 'home.html')

def registered(request):
    if logged_user(request):
        return redirect('/')
    return render(request, 'registered.html')

@require_login
def user(request, id=0):
    current_user = logged_user(request)
    # Make id an int
    id = int(id)
    # Get the user object for that id
    user = object_manager.createUser(id=id)

    # We'll show:
    # % per lang, # lists per lang, total lists, total groups, time joined,
    # % avg (any lang), # ex per lang
    browser_lang = getBrowserLanguage(request)
    # lists per lang
    pie_chart = None
    # % per lang
    bar_chart = None
    # ex per lang
    pie_chart2 = None
    if len(user.allPersonalLists()) != 0:
        lists_per_prog_lang = statistics_analyzer.AmountOfExerciseListsPerProgrammingLanguageForUser(user.id)

        pie_chart = graph_manager.makePieChart('list_per_lang', 100, 100,
                                               graphmanager.color_tuples,
                                               lists_per_prog_lang['labels'],
                                               lists_per_prog_lang['data'])

        color_info1 = graphmanager.ColorInfo("#F7464A", "#F7464A", "#FF5A5E", "#FF5A5E")
        color_info2 = graphmanager.ColorInfo("#46BFBD", "#46BFBD", "#5AD3D1", "#46BFBD")
        avg_score_per_lang = statistics_analyzer.averageScorePerProgrammingLanguageForUser(user)
        bar_chart = graph_manager.makeBarChart('score_per_lang', 200, 200,
                                               [color_info2, color_info1], avg_score_per_lang['labels'], avg_score_per_lang['data'], ["Score"], True)

        ex_per_prog_lang = statistics_analyzer.AmountOfExercisesPerProgrammingLanguageForUser(user.id)
        pie_chart2 = graph_manager.makePieChart('ex_per_lang', 100, 100,
                                               graphmanager.color_tuples,
                                               ex_per_prog_lang['labels'],
                                               ex_per_prog_lang['data'])

    if request.method == 'POST':
        if 'add_friend' in request.POST:
            current_user.addFriend(user)

        if 'remove_friend' in request.POST:
            current_user.declineFriendship(user.id)

        elif 'confirm_friendship' in request.POST:
            friend_id = request.POST.get('user_id_to_confirm')
            user.confirmFriendship(friend_id)

        elif 'decline_friendship' in request.POST:
            friend_id = request.POST.get('user_id_to_decline')
            user.declineFriendship(friend_id)

        elif 'update_profile_information' in request.POST:
            new_password1 = hashlib.md5(
                request.POST.get('new_password1').encode('utf-8')).hexdigest()

            old_password = hashlib.md5(
                request.POST.get('old_password').encode('utf-8')).hexdigest()

            if old_password == user.password:
                new_email = request.POST.get('new_email')
                user.updateProfile(new_email, new_password1)

        elif 'update_profile_picture' in request.POST:
            f = request.FILES['image']

            destination = open(
                './codegalaxy/static/profile_pictures/' + str(current_user.id) + '.png', 'wb+')

            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

            imageFile = './codegalaxy/static/profile_pictures/' + \
                str(current_user.id) + '.png'

            im1 = Image.open(imageFile)

            THUMB_SIZE = 512, 512
            image = im1.resize(THUMB_SIZE, Image.ANTIALIAS)
            image.save(
                './codegalaxy/static/profile_pictures/' + str(current_user.id) + '.png')

        elif 'confirm_membership' in request.POST:
            group_id = request.POST.get('group_id_to_confirm')
            user.confirmGroupMembership(group_id)

        elif 'decline_membership' in request.POST:
            group_id = request.POST.get('group_id_to_decline')
            user.deleteGroupMembership(group_id)

    already_friends = False
    if current_user:
        already_friends = current_user.isFriend(user)

    if user:
        group_list = user.allGroups()

        exercise_list = user.allPersonalLists()

        accepted_friendships = user.allFriendsWith()
        member_of_groups = user.allGroupsJoined()
        exercises_made = user.allExerciseListsShared(browser_lang.id)
        exercises_created = user.getAllExercisesCreated(browser_lang.id)

        if user.id != current_user.id:
            for member in member_of_groups:
                if member.group.group_type == 1:
                    member_of_groups.remove(member)

        all_data = []
        all_data.extend(accepted_friendships)
        all_data.extend(member_of_groups)
        all_data.extend(exercises_made)
        all_data.extend(exercises_created)

        all_data = sorted(all_data, key=lambda k: k.datetime, reverse=True)

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

        pending_group_memberships = []
        if current_user.id == user.id:
            pending_group_memberships = user.allPendingGroupMemberships()

        friendships = accepted_friendships
        friends = []
        for friendship in friendships:
            friends.append(
                object_manager.createUser(id=friendship.friend.id))

        mutual_friends = []
        non_mutual_friends = []
        if current_user.id != user.id:
            current_user_friend_ids = [x.id for x in current_user.allFriends()]
            for user_friend in user.allFriends():
                if user_friend.id in current_user_friend_ids:
                    mutual_friends.append(user_friend)
                else:
                    non_mutual_friends.append(user_friend)

        total_mutual_friends = len(mutual_friends)

        friendship_pending = current_user.isFriendshipPending(user)
        badges = user.getAllRewards()
        all_badges = user.getAllBadges()
        context = {'user': user, 'current_user': current_user, 'group_list': group_list, 'data': data,
                   'exercise_list': exercise_list, 'already_friends': already_friends, 'pending_group_memberships': pending_group_memberships,
                   'pending_friendships': pending_friendships, 'accepted_friendships': accepted_friendships,
                   'friends': friends, 'list_on_lang_by_user': pie_chart, 'score_per_lang': bar_chart,
                   'ex_on_lang_by_user': pie_chart2, 'total_mutual_friends': total_mutual_friends, 'mutual_friends': mutual_friends,
                   'non_mutual_friends': non_mutual_friends, 'friendship_pending': friendship_pending, 'all_badges': all_badges, 'gold_badges':badges['gold'],
                   'silver_badges': badges['silver'], 'bronze_badges': badges['bronze']}

        if current_user.id == user.id:
            context['my_profile'] = True
            context['old_email'] = user.email

        return render(request, 'user.html', context)

    else:
        return redirect('/')

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
                time.strftime("%Y-%m-%d %H:%M:%S")), str(time.strftime("%Y-%m-%d %H:%M:%S")), gender)
            object_manager.addVerification(
                email, hashlib.md5(email.encode('utf-8')).hexdigest())
            object_manager.registered(email)
            sendVerification(email)

        except:
            return render(request, 'register.html', {'error_register': True})

    return redirect('/registered/')


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
            user.checkTimeRelatedBadges()
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
    user = logged_user(request)
    browser_lang = getBrowserLanguage(request)

    group = object_manager.createGroup(id)

    user_id_to_edit = user.id

    if request.method == 'POST':
        if 'become_member' in request.POST:
            if group.membershipPending(user.id):
                user.confirmGroupMembership(group.id)
            else:
                group.insertMember(
                    user.id, 2, str(time.strftime("%Y-%m-%d %H:%M:%S")), "Member")

        elif 'add_friend' in request.POST:
            friend_id = request.POST.get('user_id_to_add', '')
            group.insertMember(
                friend_id, 2, str(time.strftime("%Y-%m-%d %H:%M:%S")), "Pending")

        elif 'update_group_picture' in request.POST:
            f = request.FILES['image']

            destination = open(
                './codegalaxy/static/group_pictures/' + str(group.id) + '.png', 'wb+')

            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

            imageFile = './codegalaxy/static/group_pictures/' + \
                str(group.id) + '.png'

            im1 = Image.open(imageFile)

            THUMB_SIZE = 512, 512
            image = im1.resize(THUMB_SIZE, Image.ANTIALIAS)
            image.save(
                './codegalaxy/static/group_pictures/' + str(group.id) + '.png')

        elif 'leave_group' in request.POST:
            group.deleteMember(user.id)

        elif 'remove_user' in request.POST:
            user_id_to_delete = request.POST.get('user_id_to_delete')
            group.deleteMember(user_id_to_delete)

        elif 'upgrade_user' in request.POST:
            user_id_to_upgrade = request.POST.get('user_id_to_upgrade')
            group.upgradeUserPermissions(user_id_to_upgrade)

        elif 'delete_group' in request.POST:
            group.disband()
            return redirect('/social/')

    is_member = False

    if group:
        user_list = group.allMembers()
        if group.group_type == 1:
            # Only users in this group can access this page
            list_owner = False
            for u in user_list:
                if u.id == user.id:
                    list_owner = True

            if not list_owner:
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

        group_owner = ''

        if group_size > 0:
            for one_user in user_list:
                exercises_made = one_user.allExerciseListsShared(browser_lang.id)
                member_of_groups = one_user.allGroupsJoined()
                accepted_friendships = one_user.allFriendsWith()
                if group.getUserPermissions(one_user.id) == 0:
                    group_owner = one_user.name()

                for member in member_of_groups:
                    if member.user.id != user.id:
                        if member.group.group_type == 1:
                            member_of_groups.remove(member)

                all_data.extend(accepted_friendships)
                all_data.extend(member_of_groups)
                all_data.extend(exercises_made)

            all_data = sorted(
                all_data, key=lambda k: k.datetime, reverse=True)

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
            for member in user_list:
                if friend.id == member.id:
                    inList = True

            if not inList:
                remaining_friends.append(friend)

        group_permissions = []
        my_user_permissions = []
        if is_member:
            group_permissions = group.getUserPermissions(user.id)
            my_user_permissions = group.getUserPermissions(user.id)
        new_user_list = []
        for group_member in user_list:
            new_user_list.append((group_member, group.getUserPermissions(group_member.id)))
        user_list = new_user_list

        group_posts = group.allPostsToHTML(user)

        context = {'user': user, 'data': data, 'id': id, 'group': group, 'user_list':
                   user_list, 'currentuser_friend_list': remaining_friends, 'is_member': is_member,
                   'group_permissions': group_permissions, 'user_id_to_edit': user_id_to_edit,
                   'my_user_permissions': my_user_permissions, 'group_size': group_size, 'group_owner': group_owner,
                   'group_posts': group_posts}
        return render(request, 'group.html', context)

    else:
        return redirect('/')


@require_login
def social(request):
    current_user = logged_user(request)

    s_term = request.POST.get('s_term', '')
    s_social = request.POST.get('s_social', 'false') != 'false'

    # Biggest Groups
    biggest_groups = statistics_analyzer.biggestGroupsTopX(5)
    color_info1 = graphmanager.ColorInfo(
        "#2a3963", "#2a3963", "#3e5084", "#3e5084")
    color_info2 = graphmanager.ColorInfo(
        "#2a3963", "#2a3963", "#3e5084", "#3e5084")
    bar_chart = graph_manager.makeBarChart('groups', 270, 180, [
                                           color_info2, color_info1], biggest_groups['labels'], biggest_groups['data'], "#members")

    context = {'biggest_groups': bar_chart, 's_term': s_term, 's_social': s_social}

    return render(request, 'groupOverview.html', context)


@require_login
def groupCreate(request, id=0):
    user = logged_user(request)
    if request.method == 'POST':
        group_name = request.POST.get('group_name', '')

        group_type = request.POST.get('group_type')

        try:
            if group_type == 'on':
                object_manager.insertGroup(
                    group_name, 1, str(time.strftime("%Y-%m-%d %H:%M:%S")))

            else:
                object_manager.insertGroup(
                    group_name, 0, str(time.strftime("%Y-%m-%d %H:%M:%S")))

            # auto add user when making a private group?
            user.createdGroup()
            group = object_manager.createGroupOnName(group_name)
            group.insertMember(
                user.id, 0, str(time.strftime("%Y-%m-%d %H:%M:%S")), 'Member')
            return redirect('/g/' + str(group.id))

        except:
            return render(request, 'groupCreate.html', {})

    return render(request, 'groupCreate.html', {})

@require_login
def badges(request):
    user = logged_user(request)
    badges = object_manager.getAllBadges()
    gold_badges = badges['gold']
    silver_badges = badges['silver']
    bronze_badges = badges['bronze']
    context = {'gold_badges': gold_badges, 'silver_badges': silver_badges, 'bronze_badges': bronze_badges}

    return render(request, 'badges.html', context)

@require_login
def badge(request, id=0):
    user = logged_user(request)
    #Omdat het kan afkljdfasfkfdas
    id = int(id)
    badge = object_manager.createBadge(id)
    users_that_earned_badge = badge.allUsersThatEarnedBadge()

    context = {'users_that_earned_badge': users_that_earned_badge, 'badge': badge}

    return render(request, 'badge.html', context)

def postNew(request):
    user = logged_user(request)
    group_id = int(request.POST.get('group_id'))
    post_text = request.POST.get('post_text')
    if post_text == '':
        return HttpResponse('')
    group = object_manager.createGroup(group_id)
    group.postOnWall(user.id, post_text)
    post = group.allPosts()[0]
    new_html = post.HTMLString(user)
    return HttpResponse(new_html)

@require_login
def replyTo(request):
    user = logged_user(request)
    group_id = int(request.POST.get('group_id'))
    post_id = int(request.POST.get('post_id'))
    post_text = request.POST.get('post_text')
    old_user_id = 0
    if post_text == '':
        return HttpResponse('')
    group = object_manager.createGroup(group_id)
    for old_post in group.allPosts():
        if old_post.id == post_id:
            old_user_id = old_post.user_id
            old_post.replyToPost(user.id, post_text)
    post = group.allPosts()[0]
    old_user = object_manager.createUser(id=old_user_id)
    new_html = post.HTMLStringReply(user, user)
    return HttpResponse(new_html)

@require_login
def deletePost(request):
    user = logged_user(request)
    group_id = int(request.POST.get('group_id'))
    post_id = int(request.POST.get('post_id'))
    group = object_manager.createGroup(group_id)
    for post in group.allPosts():
        if post.id == post_id:
            post.delete()
    return HttpResponse('')

@require_login
def editPost(request):
    user = logged_user(request)
    group_id = int(request.POST.get('group_id'))
    post_id = int(request.POST.get('post_id'))
    post_text = request.POST.get('post_text')
    group = object_manager.createGroup(group_id)
    for post in group.allPosts():
        if post.id == post_id:
            post.post_text = post_text
            post.save()
    return HttpResponse('')

def list(request, id=0):
    return render(request, 'list.html', {'id': id})


@require_login
def submit(request, id, question):
    return render(request, 'submit.html', {})


def verify(request, hash_seq):
    if object_manager.needsVerification(hash_seq):
        email = object_manager.acceptVerification(hash_seq)
        sendVerificationAccepted(email)
        object_manager.setUserActive(email)
        user = object_manager.createUser(email=email)
        return render(request, 'verify.html', {'user': user})

    return redirect('/')

def tables(request):
    import dbw
    if request.method == 'GET':
        table = request.GET.get('sql_table', '')
        if table != '':
            data = dbw.getAll(table)
            return render(request, 'tables.html', {'data': data, 'keys': data[0].keys()})
    return render(request, 'tables.html', {})
