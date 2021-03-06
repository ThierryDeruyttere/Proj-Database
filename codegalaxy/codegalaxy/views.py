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
from codegalaxy.general import getBrowserLanguage, stripStr

import os.path
from PIL import Image

# We'll use one ObjectManager to work with/create the objects stored in the DB
object_manager = objectmanager.ObjectManager()
statistics_analyzer = statisticsanalyzer.StatisticsAnalyzer()
# We'll use the graph maker to make pretty graphs with statistical data
graph_manager = graphmanager.GraphManager()

# The view for home.html
def home(request):
    current_user = logged_user(request)
    friends = []
    recommended_lists = []
    feed = []
    browser_lang = getBrowserLanguage(request)
    if current_user:
        # Als er een user bestaat de ingelogde homepage laten zien

        # Data voor op feed toevoegen
        current_user_accepted_friendships = current_user.allFriendsWith()
        current_user_member_of_groups = current_user.allGroupsJoined()
        current_user_exercises_made = current_user.allExerciseListsShared(browser_lang.id)
        current_user_exercises_created = current_user.getAllExercisesCreated(browser_lang.id)

        # Data dat niet gezien mag worden (Private group) verwijderen
        for userInGroup in current_user_member_of_groups:
            if userInGroup.group.group_type == 1:
                current_user_member_of_groups.remove(userInGroup)

        feed.extend(current_user_member_of_groups)
        feed.extend(current_user_exercises_made)
        feed.extend(current_user_exercises_created)

        # De data van elke vriend die je hebt moet ook op de feed komen
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

        # Alles moet gesorteerd worden op datum zodat alles chronologisch op het scherm kan komen
        feed = sorted(feed, key=lambda k: k.datetime, reverse=True)

        # Paginator aanmaken zodat we niet te veel data tegelijk op het scherm hebben staan maar door da pages kunnen scrollen
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

        # Aanbevolen lijsten zoeken
        recommended = recommendListsForUser(
            current_user, True, True, True, True, True, False)
        for recommended_list in recommended:
            recommended_lists.append(
                object_manager.createExerciseList(recommended_list, browser_lang.id))

        return render(request, 'home.html', {'user': current_user, 'feed_data': feed_data, 'feed': feed, 'friends': friends,
                'recommended': recommended_lists, 'random_list': imFeelingLucky(current_user)})
    # Anders de homepage waar je een account kan aanmaken en waar je kan inloggen
    return render(request, 'home.html')

# After you register for the site
def registered(request):
    if logged_user(request):
        return redirect('/')
    return render(request, 'registered.html')

# The view for user.html
@require_login
def user(request, id=0):
    current_user = logged_user(request)
    # Make id an int
    id = int(id)
    # Get the user object for that id
    user = object_manager.createUser(id=id)

    if not user:
        return redirect('/')
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
        # Here we'll create the graphs displayed on this page
        #Lists/ programming language
        lists_per_prog_lang = statistics_analyzer.AmountOfExerciseListsPerProgrammingLanguageForUser(user.id)

        pie_chart = graph_manager.makePieChart('list_per_lang', 100, 100,
                                               graphmanager.color_tuples,
                                               lists_per_prog_lang['labels'],
                                               lists_per_prog_lang['data'])

        color_info1 = graphmanager.ColorInfo("#F7464A", "#F7464A", "#FF5A5E", "#FF5A5E")
        color_info2 = graphmanager.ColorInfo("#46BFBD", "#46BFBD", "#5AD3D1", "#46BFBD")
        #Average score/ programming language
        avg_score_per_lang = statistics_analyzer.averageScorePerProgrammingLanguageForUser(user)
        bar_chart = graph_manager.makeBarChart('score_per_lang', 200, 200,
                                               [color_info2, color_info1], avg_score_per_lang['labels'], avg_score_per_lang['data'], ["Score"], True)

        # Exercises/ programming language
        ex_per_prog_lang = statistics_analyzer.AmountOfExercisesPerProgrammingLanguageForUser(user.id)
        pie_chart2 = graph_manager.makePieChart('ex_per_lang', 100, 100,
                                               graphmanager.color_tuples,
                                               ex_per_prog_lang['labels'],
                                               ex_per_prog_lang['data'])

    if request.method == 'POST':
        # Verschillende POST requests voor elke actie die aan een knop verbonden is
        # Adding a new friend (sending request)
        if 'add_friend' in request.POST:
            current_user.addFriend(user)

        # Removing a friend
        if 'remove_friend' in request.POST:
            current_user.declineFriendship(user.id)

        # Accept friend request
        elif 'confirm_friendship' in request.POST:
            friend_id = request.POST.get('user_id_to_confirm')
            user.confirmFriendship(friend_id)

        # Decline friend request
        elif 'decline_friendship' in request.POST:
            friend_id = request.POST.get('user_id_to_decline')
            user.declineFriendship(friend_id)

        # Change your profile info (pass/email/...)
        elif 'update_profile_information' in request.POST:
            new_password1 = hashlib.md5(
                request.POST.get('new_password1').encode('utf-8')).hexdigest()

            old_password = hashlib.md5(
                request.POST.get('old_password').encode('utf-8')).hexdigest()

            if old_password == user.password:
                new_email = request.POST.get('new_email')
                user.updateProfile(new_email, new_password1)

        # Change your photo
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

            # Deze foto zal automatisch naar 512x512 pixels worden omgezet
            THUMB_SIZE = 512, 512
            image = im1.resize(THUMB_SIZE, Image.ANTIALIAS)
            image.save(
                './codegalaxy/static/profile_pictures/' + str(current_user.id) + '.png')

        # Accepting a group invite
        elif 'confirm_membership' in request.POST:
            group_id = request.POST.get('group_id_to_confirm')
            user.confirmGroupMembership(group_id)

        # Declining a group invite
        elif 'decline_membership' in request.POST:
            group_id = request.POST.get('group_id_to_decline')
            user.deleteGroupMembership(group_id)

    # Data voor de add-user knop
    already_friends = False
    if current_user:
        # Checking if you and the user which profile you are looking at are friends
        already_friends = current_user.isFriend(user)

    if user:
        group_list = user.allGroups()

        exercise_list = user.allPersonalLists()

        # Data voor de feed
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

        # Data voor de feed sorteren op datum
        all_data = sorted(all_data, key=lambda k: k.datetime, reverse=True)

        # Paginator aanmaken om data per pagina te beperken
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

        # Welke users willen je toevoegen
        pending_friendships = []
        if current_user.id == user.id:
            pending_friendships = user.allPendingFriendships()

        # Welke groepen willen je als lid hebben
        pending_group_memberships = []
        if current_user.id == user.id:
            pending_group_memberships = user.allPendingGroupMemberships()

        # Al je vrienden
        friendships = accepted_friendships
        friends = []
        for friendship in friendships:
            friends.append(
                object_manager.createUser(id=friendship.friend.id))

        # Als dit niet je eigen profiel is kan je zien met wie je al bevriend bent
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
        # Alls badges die de user heeft
        badges = user.getAllRewards()
        all_badges = user.getAllBadges()
        context = {'user': user, 'current_user': current_user, 'group_list': group_list, 'data': data,
                   'exercise_list': exercise_list, 'already_friends': already_friends, 'pending_group_memberships': pending_group_memberships,
                   'pending_friendships': pending_friendships, 'accepted_friendships': accepted_friendships,
                   'friends': friends, 'list_on_lang_by_user': pie_chart, 'score_per_lang': bar_chart,
                   'ex_on_lang_by_user': pie_chart2, 'total_mutual_friends': total_mutual_friends, 'mutual_friends': mutual_friends,
                   'non_mutual_friends': non_mutual_friends, 'friendship_pending': friendship_pending, 'all_badges': all_badges, 'gold_badges': badges['gold'],
                   'silver_badges': badges['silver'], 'bronze_badges': badges['bronze']}

        if current_user.id == user.id:
            context['my_profile'] = True
            context['old_email'] = user.email

        return render(request, 'user.html', context)

# Logging on to the site
def login(request):
    # Adding an entry for the current user in the request.session table
    if 'current_user' not in request.session:
        request.session['current_user'] = None

    # There has been a request to log in
    if request.method == 'POST':
        # And thus we verify the password
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


# Logging off from the site
@require_login('/')
def logout(request):
    # Flush deletes your entry from the request.session table
    request.session.flush()
    request.session['current_user'] = None
    return render(request, 'logout.html', {})


# A redirect to your own user page
@require_login
def me(request):
    user_url = '/u/{id}'.format(id=logged_user(request).id)
    return redirect(user_url)

# The view for the group.html page
@require_login
def group(request, id=0):
    user = logged_user(request)
    browser_lang = getBrowserLanguage(request)
    group = object_manager.createGroup(id)
    user_id_to_edit = user.id

    # Interacting with the page
    # If the logged user wants to join this group
    if request.method == 'POST':
        if 'become_member' in request.POST:
            # If you were invited
            if group.membershipPending(user.id):
                user.confirmGroupMembership(group.id)
            # If you were not invited
            else:
                group.insertMember(
                    user.id, 2, str(time.strftime("%Y-%m-%d %H:%M:%S")), "Member")

        # If you want to add someone to this group
        elif 'add_friend' in request.POST:
            friend_id = request.POST.get('user_id_to_add', '')
            group.insertMember(
                friend_id, 2, str(time.strftime("%Y-%m-%d %H:%M:%S")), "Pending")

        # If you are an admin/the owner, you may choose to upload a new photo
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

        # If you want to leave the group
        elif 'leave_group' in request.POST:
            if group.getUserPermissions(user.id) == 0:
                group.disband()
                return redirect('/social/')
            else:
                group.deleteMember(user.id)

        # If the owner or an admin decides to remove a user from the group
        elif 'remove_user' in request.POST:
            user_id_to_delete = request.POST.get('user_id_to_delete')
            group.deleteMember(user_id_to_delete)

        # If a user gets upgraded to admin
        elif 'upgrade_user' in request.POST:
            user_id_to_upgrade = request.POST.get('user_id_to_upgrade')
            group.upgradeUserPermissions(user_id_to_upgrade)

        # If the owner wants to delete the group
        elif 'delete_group' in request.POST:
            group.disband()
            return redirect('/social/')

    is_member = False

    if group:
        user_list = group.allMembers()

        # If the group is private, only members can access this page
        if group.group_type == 1:
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

        # Check if current user is member of this group
        if group_size > 0:
            for x in range(0, group_size):
                if user.email == user_list[x].email:
                    is_member = True

        accepted_friendships = []
        member_of_groups = []
        exercises_made = []
        all_data = []

        group_owner = ''

        # Sets up a list with all data (friendships, members, exercises) to display on the group feed
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

        # Ceates list of all friends who are not a member of this group yet
        remaining_friends = []
        for friend in currentuser_friend_list:
            inList = False
            for member in user_list:
                if friend.id == member.id:
                    inList = True

            if not inList:
                remaining_friends.append(friend)

        # Specifies users permissions in a group
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

# Set-up social page
@require_login
def social(request):
    current_user = logged_user(request)

    s_term = request.POST.get('s_term', '')
    s_social = request.POST.get('s_social', 'false') != 'false'

    # Sets up 'Biggest Groups' statistics
    biggest_groups = statistics_analyzer.biggestGroupsTopX(5)
    color_info1 = graphmanager.ColorInfo(
        "#2a3963", "#2a3963", "#3e5084", "#3e5084")
    color_info2 = graphmanager.ColorInfo(
        "#2a3963", "#2a3963", "#3e5084", "#3e5084")
    bar_chart = graph_manager.makeBarChart('groups', 270, 180, [
                                           color_info2, color_info1], biggest_groups['labels'], biggest_groups['data'], "#members")

    # Lists containing all friend or group notifications to use on html page
    friend_requests = current_user.allPendingFriendships()
    group_requests = current_user.allPendingGroupMemberships()

    context = {'biggest_groups': bar_chart, 's_term': s_term, 's_social': s_social, 'friend_requests': friend_requests, 'group_requests': group_requests}

    return render(request, 'groupOverview.html', context)

# Create a new group
@require_login
def groupCreate(request, id=0):
    user = logged_user(request)

    # Determine group name and type (private or public)
    if request.method == 'POST':
        group_name = request.POST.get('group_name', '')

        group_type = request.POST.get('group_type')

        try:
            # Create private group
            if group_type == 'on':
                object_manager.insertGroup(
                    group_name, 1, str(time.strftime("%Y-%m-%d %H:%M:%S")))

            # Create public group
            else:
                object_manager.insertGroup(
                    group_name, 0, str(time.strftime("%Y-%m-%d %H:%M:%S")))

            # User becomes owner and member of new created group
            user.createdGroup()
            group = object_manager.createGroupOnName(group_name)
            group.insertMember(
                user.id, 0, str(time.strftime("%Y-%m-%d %H:%M:%S")), 'Member')
            return redirect('/g/' + str(group.id))

        except:
            return render(request, 'groupCreate.html', {})

    return render(request, 'groupCreate.html', {})

# Set-up badges page
@require_login
def badges(request):
    user = logged_user(request)

    # Lis of all badges
    badges = object_manager.getAllBadges()
    badge_types = ['custom', 'memberOfGroup', 'hasFriend', 'solvedList', 'createdList', 'peopleSolvedMyList', 'gaveRating', 'timeMember', 'frequentVisitor']
    context = {'badge_types': badge_types, 'badges': badges}

    return render(request, 'badges.html', context)

# Set-up page for each badge
@require_login
def badge(request, id=0):
    user = logged_user(request)
    id = int(id)
    badge = object_manager.createBadge(id)
    browser_lang = getBrowserLanguage(request)

    # Get information about badge (users who earned the badge, percentage of completion,...)
    if badge:
        users_that_earned_badge = badge.allUsersThatEarnedBadge()
        target_score = badge.target_value
        if browser_lang.code == "en":
            message = badge.getEnglishMessage()
        elif browser_lang.code == "nl":
            message = badge.getDutchMessageTranslation()
        try:
            current_score = user.getCurrentValueForBadge(badge.id)
        except:
            current_score = 0
        percentage_finished = round((current_score / badge.target_value) * 100)
        if percentage_finished > 100:
            percentage_finished = 100

        context = {'users_that_earned_badge': users_that_earned_badge, 'badge': badge, 'percentage_finished': percentage_finished, 'current_score': current_score,
                   'target_score': target_score, 'message': message}

        return render(request, 'badge.html', context)
    else:
        return redirect("/badges/")

# Post new message to wall
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

# Reply to a post on a group wall
@require_login
def replyTo(request):
    user = logged_user(request)

    # Get the right group & post id's
    group_id = int(request.POST.get('group_id'))
    post_id = int(request.POST.get('post_id'))
    post_text = request.POST.get('post_text')
    old_user_id = 0

    # Return if post is empty
    if post_text == '':
        return HttpResponse('')
    group = object_manager.createGroup(group_id)

    # Search to post to reply to and write reply
    for old_post in group.allPosts():
        if old_post.id == post_id:
            old_user_id = old_post.user_id
            old_post.replyToPost(user.id, post_text)
    post = group.allPosts()[0]
    old_user = object_manager.createUser(id=old_user_id)
    new_html = post.HTMLStringReply(user, user)
    return HttpResponse(new_html)

# Delete post from group wall
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

# Edit a post on a group wall
@require_login
def editPost(request):
    import markdown2
    markdown_converter = markdown2.Markdown()
    user = logged_user(request)

    # Get the right post & group
    group_id = int(request.POST.get('group_id'))
    post_id = int(request.POST.get('post_id'))
    post_text = request.POST.get('post_text')
    group = object_manager.createGroup(group_id)

    # Edit post
    for post in group.allPosts():
        if post.id == post_id:
            post.post_text = post_text
            post.save()
            post_html = markdown_converter.convert(post_text)

            return HttpResponse(post_html)

@require_login
def wantToEdit(request):
    group_id = int(request.POST.get('group_id'))
    post_id = int(request.POST.get('post_id'))
    group = object_manager.createGroup(group_id)
    for post in group.allPosts():
        if post.id == post_id:
            return HttpResponse(stripStr(post.post_text))
    return HttpResponse("")

# Verify email
def verify(request, hash_seq):
    if object_manager.needsVerification(hash_seq):
        email = object_manager.acceptVerification(hash_seq)
        sendVerificationAccepted(email)
        object_manager.setUserActive(email)
        user = object_manager.createUser(email=email)
        return render(request, 'verify.html', {'user': user})
    return redirect('/')
