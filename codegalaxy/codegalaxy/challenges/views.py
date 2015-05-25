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


# Fetches tha names and pictures (path) of all the users except one
def getAllUsersNames(except_user):
    all_users = object_manager.allUsers()
    all_users_names = []
    for i in all_users:
        if i.id == except_user:
            continue

        name = i.first_name + " " + i.last_name
        # The pictures are located in the 'static' folder
        img = "/static/" + i.getPicture()
        all_users_names.append({"value": name, "data": img})
    return all_users_names

# Maps the Exerciselist-objects on the programming languages
# NOTE: These Exerciselists are the ones neither user has made (used for challenges).
def prepareDict(lists):
    new_dict = {}
    for i in lists:
        if i.programming_language.name not in new_dict:
            new_dict[i.programming_language.name] = []
        new_dict[i.programming_language.name].append([i.id, i.name])

    if len(new_dict) == 0:
        return {'empty': [[-1, _("Sorry, we couldn't find any lists!")]]}

    return new_dict

# Goes over a list of challenge-objects of 2 different types and counts how
# many there are of each type
def getFinishedChallengesStats(challenges):
    stats = {"Score": 0, "Perfects": 0}
    for i in challenges:
        stats[i.challenge_type.type] += 1
    return stats

# Shows head-to-head record of two users in a graph
def createPieChart(user, challenged, browser_language):
    # Get charts info
    my_wins = challenge_manager.getWinsAgainst(user.id, challenged.id)
    opponent_wins = challenge_manager.getWinsAgainst(challenged.id, user.id)
    pie_chart = graph_manager.makePieChart("#wins", 150, 150, graphmanager.color_tuples,
                                           ["You", challenged.first_name + " " + challenged.last_name], [my_wins, opponent_wins])
    pie_chart = graph_manager.addTitle(pie_chart, _("Wins per user"))
    return pie_chart

# Shows how many challenges of eacht type you have done against another user
def createBarChart(user, challenged, browser_language):
    finished_challenges = challenge_manager.getFinishedChallengesBetween(user.id, challenged.id, browser_language.id)
    stats = getFinishedChallengesStats(finished_challenges)

    color_info1 = graphmanager.ColorInfo("#f04124", "#f04124", "#f76148", "#f76148")
    color_info2 = graphmanager.ColorInfo("#FF9437", "#FF9437", "#ffa85d", "#ffa85d")

    values = [[]]
    for v in stats.values():
        values[0].append(v)

    bar_chart = graph_manager.makeBarChart("#challenge-per-challenge_type", 200, 200, [color_info1, color_info2], stats.keys(), values, ["test"])
    bar_chart = graph_manager.addTitle(bar_chart, _("#Challenges per challenge type"))
    return bar_chart

# Searches all the lists between two users that are still egligable for
# a challenge (not currently busy, already done,...)
def getRemainingLists(user, challenged, browser_language):
    user_pers_lists = user.allPersonalLists()
    # Get all the list objects from the personal lists
    user_lists = [i.exercises_list for i in user_pers_lists]

    challenged_pers_lists = challenged.allPersonalLists()
    # Same here
    challenged_lists = [i.exercises_list for i in challenged_pers_lists]

    all_lists = object_manager.getAllExerciseLists(browser_language.id)
    # take an union from all solved lists + lists created by the users
    active_challenges = challenge_manager.getChallengesBetween(user.id, challenged.id, browser_language.id)
    active_lists = [i.list.id for i in active_challenges]

    union = set(user_lists) | set(challenged_lists) | set(user.getAllCreatedLists(browser_language.id)) | \
        set(challenged.getAllCreatedLists(browser_language.id)) | set(active_challenges)

    intersect = set(all_lists) - set(union)
    remaining_lists = []
    for i in intersect:
        if i.id not in active_lists:
            remaining_lists.append(i)
    return remaining_lists

@require_login
# The view for challenges.html
def challenges(request):
    browser_language = getBrowserLanguage(request)
    user = logged_user(request)
    all_users_names = getAllUsersNames(user.id)

    # We'll fetch all the pending requests for challenges for the current user
    challenge_requests = challenge_manager.getChallengeRequestsForUser(user.id, browser_language.id)

    if request.method == 'POST':
        challenged_name = request.POST.get('challenged')
        challenged = object_manager.getUserByName(challenged_name)
        challenge_type = request.POST.get('challenge_type')
        challenge_list = request.POST.get('possible_lists')
        challenged_list_obj = object_manager.createExerciseList(int(challenge_list), browser_language.id)
        challenge_manager.createChallenge(user.id, challenged.id, challenge_type, challenged_list_obj.id)
        return HttpResponseRedirect('')

    if request.method == 'GET' and 'available_lists' in request.GET:
        challenged = object_manager.getUserByName(request.GET.get('challenged'))
        remaining_lists = getRemainingLists(user, challenged, browser_language)

        # Get charts info & prepare dictionary

        dump = prepareDict(remaining_lists)
        dump['wins_chart'] = createPieChart(user, challenged, browser_language)
        dump['challenges_chart'] = createBarChart(user, challenged, browser_language)

        return HttpResponse(json.dumps(dump))

    return render(request, 'challenges.html', {"all_users_names": json.dumps(all_users_names),
                                               "user": user,
                                               "challenge_requests": challenge_requests
                                               })

# The POST request sent when a user reacts to a request/running challenge.
# This updates whether the user accepts, cancels or gives up on the challenge.
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

# The html to be inserted for any challenges that are still going on,
# contains info like between who the challenge is/which list/type/...
def createActiveHTML(challenge):
    return """
    <div class="large-12 columns">
    <div class="panel radius challenge" id="{challenger.id}-{challenged.id}-{list.id}">
        <ul class="large-block-grid-3">
            <li><b>{challenger_text}</b><br/>
                <img class="challengers-small" src="/static/{challenger_pict}"><br/>
                <b>{challenger.first_name} {challenger.last_name}</b>
            </li>
            <li>
                <b>{challenge_info_string}</b><br/>
                Type: {type}<br/>
                <a href="/l/{list.id}">{list.name}</a><br/>
                <button class="alert radius tiny give_up" name="{challenger.id}-{challenged.id}-{list.id}">{give_up_string}</button>
                </li>
            <li>
                <b>{opponent_string}</b><br/>
                <img class="challengers-small" src="/static/{challenged_pict}"><br/>
                <b>{challenged.first_name} {challenged.last_name}</b>
            </li>
        </ul>
    </div>
    </div>""".format(challenged_pict=challenge.challenged.getPicture(), challenger_pict=challenge.challenger.getPicture(),
                     challenger=challenge.challenger, challenged=challenge.challenged,
                     type=challenge.challenge_type.type, list=challenge.list,
                     challenge_info_string=_("Challenge info..."), give_up_string=_("Give up"),
                     opponent_string=_("Opponent"), challenger_text=_("Challenger"))

# Gets all the challenges a certain user is busy with right now (not completed)
def get_actives(request):
    browser_language = getBrowserLanguage(request)
    user = request.GET.get('user')
    actives = challenge_manager.getActiveChallengesForUser(int(user), browser_language.id)
    html = ""
    for i in actives:
        html += createActiveHTML(i)

    return HttpResponse(html)

# Get the score text for users
def getScoreText(challenge, challenger_score, challenged_score):
    challenger_score_text = ""
    challenged_score_text = ""

    if challenger_score == -1 and challenged_score == -1:
        if challenge.winner.id == challenge.challenger.id:
            return _("Won by default"), _("Gave up")
        else:
             return _("Gave up"), _("Won by default")
    if challenge.challenge_type.code == 1:
        #Score
        challenger_score_text += str(challenger_score) + "%"
        challenged_score_text += str(challenged_score) + "%"
    elif challenge.challenge_type.code == 2:
        challenger_score_text += str(challenger_score) + _(" Perfects")
        challenged_score_text += str(challenged_score) + _(" Perfects")

    return challenger_score_text, challenged_score_text

# The html to be inserted for any completed challenges, contains info
# like who won/which list/type/...
def createFinishedHtml(challenge):
    challenger_score = challenge.getScoreFor(challenge.challenger)
    challenged_score = challenge.getScoreFor(challenge.challenged)

    challenger_score_text, challenged_score_text = getScoreText(challenge, challenger_score, challenged_score)

    if challenge.challenger.id == challenge.winner.id:
        return """
        <div class="large-12 columns">
        <div class="panel radius challenge finished">
             <ul class="large-block-grid-3">
                <li>
                    <b class="success-text">{winner_text}</b><br/>
                    <img class="challengers-small victor" src="/static/{challenger_pict}"><br/>
                    <b>{challenger.first_name} {challenger.last_name}</b><br/>
                    {challenger_score_text}
                </li>
                <li>
                    <b>{challenge_info_string}</b><br/>
                    Type: {type}<br/>
                    <a href="/l/{list.id}">{list.name}</a>
                    </li>
                <li>
                    <b class="alert-text">{loser_text}</b><br/>
                    <img class="challengers-small loser" src="/static/{challenged_pict}"><br/>
                    <b>{challenged.first_name} {challenged.last_name}</b><br/>
                    {challenged_score_text}
                </li>
            </ul>
        </div>
        </div>""".format(challenged_pict=challenge.challenged.getPicture(), challenger_pict=challenge.challenger.getPicture(),
                         challenger=challenge.challenger, challenged=challenge.challenged,
                         type=challenge.challenge_type.type, list=challenge.list, winner_text=_("Winner"),
                         loser_text=_("Loser"),challenge_info_string=_("Challenge info..."),
                         challenger_score_text = challenger_score_text, challenged_score_text = challenged_score_text)
    else:
        return """
        <div class="large-12 columns">
        <div class="panel radius challenge finished">
             <ul class="large-block-grid-3">
                <li><b class="alert-text">{loser_text}</b><br/>
                    <img class="challengers-small loser" src="/static/{challenger_pict}"><br/>
                    <b>{challenger.first_name} {challenger.last_name}</b><br/>
                    {challenger_score_text}
                </li>
                <li>
                    <b>{challenge_info_string}</b><br/>
                    {type_string} {type}<br/>
                    {list_string} <a href="/l/{list.id}">{list.name}</a>
                    </li>
                <li>
                    <b class="success-text">{winner_text}</b><br/>
                    <img class="challengers-small victor" src="/static/{challenged_pict}"><br/>
                    <b>{challenged.first_name} {challenged.last_name}</b><br/>
                    {challenged_score_text}
                </li>
            </ul>
        </div>
        </div>""".format(challenged_pict=challenge.challenged.getPicture(), challenger_pict=challenge.challenger.getPicture(),
                         challenger=challenge.challenger, challenged=challenge.challenged,
                         type=challenge.challenge_type.type, list=challenge.list, winner_text=_("Winner"),
                         loser_text=_("Loser"), challenge_info_string=_("Challenge info..."),
                         type_string=_("Type:"), list_string=_("List:"),
                         challenger_score_text = challenger_score_text, challenged_score_text = challenged_score_text)

# Seeks out which challenges have een completed and chains the appropriate
# html together
def get_finished(request):
    browser_language = getBrowserLanguage(request)
    user = request.GET.get('user')
    completed = challenge_manager.getFinishedChallengesForUser(int(user), browser_language.id)
    html = ""
    for i in completed:
        html += createFinishedHtml(i)

    return HttpResponse(html)

# The html to be inserted for any challenge requests (accept button/some info/...)
def createRequestHTML(challenge, user):
    request_type = "Request"
    buttons = '<button type="button" class="alert small radius challenge_cancel" name="{challenger.id}-{challenged.id}-{list.id}">' + _("Cancel") + '</button>'
    if challenge.challenger.id != user.id:
        request_type = _("Invite")
        buttons = '<button type="button" class="success small radius challenge_accept" name="{challenger.id}-{challenged.id}-{list.id}">' + _("Accept") + '</button>' + buttons

    buttons = buttons.format(challenger=challenge.challenger, challenged=challenge.challenged,
                             list=challenge.list)

    return """
    <div class="large-12 columns">
    <div class="panel radius challenge" id="request{challenger.id}-{challenged.id}-{list.id}">
        <ul class="large-block-grid-3">
            <li><b>{challenger_string}</b><br/>
                <img class="challengers-small" src="/static/{challenger_pict}"><br/>
                <b>{challenger.first_name} {challenger.last_name}</b>
            </li>
            <li>
                <h4><b>{request_type}</b></h4><br/>
                {type_string} {type}<br/>
                {list_string} <a href="/l/{list.id}">{list.name}</a>
                <br/><br/>
                {buttons}
                </li>
            <li>
                <b>{opponent_string}</b><br/>
                <img class="challengers-small" src="/static/{challenged_pict}"><br/>
                <b>{challenged.first_name} {challenged.last_name}</b>
            </li>
        </ul>
    </div>
    </div>""".format(challenged_pict=challenge.challenged.getPicture(), challenger_pict=challenge.challenger.getPicture(),
                     challenger=challenge.challenger, challenged=challenge.challenged,
                     type=challenge.challenge_type.type, list=challenge.list,
                     buttons=buttons, request_type=request_type, challenger_string=_("Challenger"),
                     opponent_string=_("Opponent"), type_string=_("Type:"), list_string=_("List:"))

# Seeks out which challenges have een requested and chains the appropriate
# html together
def get_requests(request):
    browser_language = getBrowserLanguage(request)
    user = logged_user(request)

    completed = challenge_manager.getChallengeRequestsForUser(user.id, browser_language.id)
    html = ""
    for i in completed:
        html += createRequestHTML(i, user)

    return HttpResponse(html)
