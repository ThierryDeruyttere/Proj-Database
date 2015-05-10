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
from managers.gm import graphmanager
import json
from codegalaxy.general import getBrowserLanguage
object_manager = objectmanager.ObjectManager()
challenge_manager = challengemanager.ChallengeManager()
graph_manager = graphmanager.GraphManager()


def getAllUsersNames(except_user):
    all_users = object_manager.allUsers()
    all_users_names = []
    for i in all_users:
        if i.id == except_user:
            continue

        name = i.first_name + " " + i.last_name
        img = "/static/" + i.getPicture()
        all_users_names.append({"value": name, "data": img})
    return all_users_names

def prepareDict(lists):
    new_dict = {}
    for i in lists:
        if i.programming_language.name not in new_dict:
            new_dict[i.programming_language.name] = []
        new_dict[i.programming_language.name].append(i.name)

    return new_dict

def getListFromName(list_name, language_code):
    lists = object_manager.getAllExerciseLists(language_code)
    for i in lists:
        if i.name == list_name:
            return i
    return None


def getFinishedChallengesStats(challenges):
    stats = {"Score":0, "Perfects":0}
    for i in challenges:

        stats[i.challenge_type.type] += 1
    return stats


@require_login
def challenges(request):
    browser_language = getBrowserLanguage(request)
    user = logged_user(request)
    all_users_names = getAllUsersNames(user.id)

    challenge_requests = challenge_manager.getChallengeRequestsForUser(user.id, browser_language.id)

    if request.method == 'POST':
        challenged_name = request.POST.get('challenged')
        challenged = object_manager.getUserByName(challenged_name)
        challenge_type = request.POST.get('challenge_type')
        challenge_list = request.POST.get('possible_lists')
        challenged_list_obj = getListFromName(challenge_list, browser_language.id)
        challenge_manager.createChallenge(user.id, challenged.id, challenge_type, challenged_list_obj.id)
        return HttpResponseRedirect('')

    if request.method == 'GET' and 'available_lists' in request.GET:
        user_pers_lists = user.allPersonalLists()
        #Get all the list objects from the personal lists
        user_lists = [i.exercises_list for i in user_pers_lists]

        challenged = object_manager.getUserByName(request.GET.get('challenged'))
        challenged_pers_lists = challenged.allPersonalLists()
        #Same here
        challenged_lists = [i.exercises_list for i in challenged_pers_lists]

        all_lists = object_manager.getAllExerciseLists(browser_language.id)
        #take an union from all solved lists + lists created by the users
        active_challenges = challenge_manager.getChallengesBetween(user.id, challenged.id, browser_language.id)
        active_lists = [i.list.id for i in active_challenges]

        union = set(user_lists) | set(challenged_lists) | set(user.getAllCreatedLists(browser_language.id)) | \
                set(challenged.getAllCreatedLists(browser_language.id)) | set(active_challenges)

        intersect = set(all_lists) - set(union)
        remaining_lists = []
        for i in intersect:
            if i.id not in active_lists:
                remaining_lists.append(i)

        #Get charts info
        my_wins  = challenge_manager.getWinsAgainst(user.id, challenged.id)
        opponent_wins = challenge_manager.getWinsAgainst(challenged.id, user.id)
        pie_chart = graph_manager.makePieChart("#wins", 150,150, graphmanager.color_tuples,
                                               ["You", challenged.first_name + " " + challenged.last_name] , [my_wins, opponent_wins],
                                               "Wins per user")
        dump = prepareDict(remaining_lists)
        dump['wins_chart'] = pie_chart

        finished_challenges = challenge_manager.getFinishedChallengesBetween(user.id, challenged.id, browser_language.id)
        stats = getFinishedChallengesStats(finished_challenges)

        color_info1 = graphmanager.ColorInfo("#f04124", "#f04124", "#f76148", "#f76148")
        color_info2 = graphmanager.ColorInfo("#FF9437", "#FF9437", "#ffa85d", "#ffa85d")

        values = [[]]
        for v in stats.values():
            values[0].append(v)

        bar_chart = graph_manager.makeBarChart("#challenge-per-challenge_type", 200, 200, [color_info1, color_info2], stats.keys() , values, ["test"], "#Challenges per challenge type")
        dump['challenges_chart'] = bar_chart

        return HttpResponse(json.dumps(dump))

    return render(request, 'challenges.html', {"all_users_names": json.dumps(all_users_names),
                                               "user": user,
                                               "challenge_requests": challenge_requests
                                               })

def handle_request(request):
    info = request.POST.get('challenge_info')
    challenge_info = info.split('-')
    challenger = int(challenge_info[0])
    challenged = int(challenge_info[1])
    challenge_list = int(challenge_info[2])
    user = logged_user(request)

    if request.POST.get('cancel', None):
        challenge_manager.cancelChallenge(challenger, challenged, challenge_list)

    elif request.POST.get('accept', None):
        challenge_manager.acceptChallenge(challenger, challenged, challenge_list)

    elif request.POST.get('give_up', None):
        challenge_manager.giveUpChallenge(user.id, challenger, challenged, challenge_list)

    return HttpResponse()

def createActiveHTML(challenge):

    return """
    <div class="large-12 columns large-centered">
    <div class="panel radius challenge" id="{challenger.id}-{challenged.id}-{list.id}">
        <ul class="large-block-grid-3">
            <li><b>Challenger</b><br/>
                <img class="challengers-small" src="/static/{challenger_pict}"><br/>
                <b>{challenger.first_name} {challenger.last_name}</b>
            </li>
            <li>
                <b>Challenge info...</b><br/>
                Type: {type}<br/>
                <a href="/l/{list.id}">{list.name}</a><br/>
                <button class="alert radius tiny give_up" name="{challenger.id}-{challenged.id}-{list.id}">Give up</button>
                </li>
            <li>
                <b>Opponent</b><br/>
                <img class="challengers-small" src="/static/{challenged_pict}"><br/>
                <b>{challenged.first_name} {challenged.last_name}</b>
            </li>
        </ul>
    </div>
    </div>""".format(challenged_pict = challenge.challenged.getPicture(), challenger_pict = challenge.challenger.getPicture(),
                     challenger= challenge.challenger, challenged = challenge.challenged,
                     type = challenge.challenge_type.type, list=challenge.list)



def get_actives(request):
    browser_language = getBrowserLanguage(request)
    user = request.GET.get('user')
    actives = challenge_manager.getActiveChallengesForUser(int(user), browser_language.id)
    html = ""
    for i in actives:
        html += createActiveHTML(i)

    return HttpResponse(html)


def createFinishedHtml(challenge):

    if challenge.challenger.id == challenge.winner.id:
        return """
        <div class="large-12 columns large-centered">
        <div class="panel radius challenge finished">
             <ul class="large-block-grid-3">
                <li>
                    <b class="success-text">Winner</b><br/>
                    <img class="challengers-small victor" src="/static/{challenger_pict}"><br/>
                    <b>{challenger.first_name} {challenger.last_name}</b><br/>
                </li>
                <li>
                    <b>Challenge info...</b><br/>
                    Type: {type}<br/>
                    <a href="/l/{list.id}">{list.name}</a>
                    </li>
                <li>
                    <b class="alert-text">Loser</b><br/>
                    <img class="challengers-small loser" src="/static/{challenged_pict}"><br/>
                    <b>{challenged.first_name} {challenged.last_name}</b><br/>
                </li>
            </ul>
        </div>
        </div>""".format(challenged_pict = challenge.challenged.getPicture(), challenger_pict = challenge.challenger.getPicture(),
                   challenger= challenge.challenger, challenged = challenge.challenged,
                   type = challenge.challenge_type.type, list=challenge.list)
    else:
        return """
        <div class="large-12 columns large-centered">
        <div class="panel radius challenge finished">
             <ul class="large-block-grid-3">
                <li><b class="alert-text">Loser</b><br/>
                    <img class="challengers-small loser" src="/static/{challenger_pict}"><br/>
                    <b>{challenger.first_name} {challenger.last_name}</b><br/>
                </li>
                <li>
                    <b>Challenge info...</b><br/>
                    Type: {type}<br/>
                    <a href="/l/{list.id}">{list.name}</a>
                    </li>
                <li>
                    <b class="success_text">Winner</b><br/>
                    <img class="challengers-small victor" src="/static/{challenged_pict}"><br/>
                    <b>{challenged.first_name} {challenged.last_name}</b><br/>

                </li>
            </ul>
        </div>
        </div>""".format(challenged_pict = challenge.challenged.getPicture(), challenger_pict = challenge.challenger.getPicture(),
                   challenger= challenge.challenger, challenged = challenge.challenged,
                   type = challenge.challenge_type.type, list=challenge.list)

def get_finished(request):
    browser_language = getBrowserLanguage(request)
    user = request.GET.get('user')
    completed = challenge_manager.getFinishedChallengesForUser(int(user), browser_language.id)
    html = ""
    for i in completed:
        html += createFinishedHtml(i)

    return HttpResponse(html)

def createRequestHTML(challenge, user):
    request_type = "request"
    buttons = """<button type="button" class="alert small radius challenge_cancel" name="{challenger.id}-{challenged.id}-{list.id}">Cancel</button>"""
    if challenge.challenger.id != user.id:
        request_type = "invite"
        buttons = """<button type="button" class="success small radius challenge_accept" name="{challenger.id}-{challenged.id}-{list.id}">Accept</button>
                      """ + buttons

    buttons = buttons.format(challenger= challenge.challenger, challenged = challenge.challenged,
                     list=challenge.list)

    return """
    <div class="large-12 columns large-centered">
    <div class="panel radius challenge" id="request{challenger.id}-{challenged.id}-{list.id}">
        <ul class="large-block-grid-3">
            <li><b>Challenger</b><br/>
                <img class="challengers-small" src="/static/{challenger_pict}"><br/>
                <b>{challenger.first_name} {challenger.last_name}</b>
            </li>
            <li>
                <h4><b>{request_type}</b></h4><br/>
                Type: {type}<br/>
                List: <a href="/l/{list.id}">{list.name}</a>
                <br/><br/>
                {buttons}
                </li>
            <li>
                <b>Opponent</b><br/>
                <img class="challengers-small" src="/static/{challenged_pict}"><br/>
                <b>{challenged.first_name} {challenged.last_name}</b>
            </li>
        </ul>
    </div>
    </div>""".format(challenged_pict = challenge.challenged.getPicture(), challenger_pict = challenge.challenger.getPicture(),
                     challenger= challenge.challenger, challenged = challenge.challenged,
                     type = challenge.challenge_type.type, list=challenge.list,
                     buttons=buttons, request_type=request_type)


def get_requests(request):
    browser_language = getBrowserLanguage(request)
    user = logged_user(request)

    completed = challenge_manager.getChallengeRequestsForUser(user.id, browser_language.id)
    html = ""
    for i in completed:
        html += createRequestHTML(i, user)

    return HttpResponse(html)
