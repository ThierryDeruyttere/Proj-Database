from django.core.context_processors import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.translation import ugettext as _

import time
import json
from codegalaxy.general import getBrowserLanguage

from pymysql import escape_string

from managers.om import *
from managers.gm import *
from managers.om.exercise import Question
from managers.rm.recommendations import *

from codegalaxy.authentication import require_login, logged_user
from codegalaxy.evaluation.evaluators import *
from managers.cm import challengemanager

object_manager = objectmanager.ObjectManager()
statistics_analyzer = statisticsanalyzer.StatisticsAnalyzer()
graph_manager = graphmanager.GraphManager()
challenge_manager = challengemanager.ChallengeManager()

# Remove a certain language from a list
# This is necessary for when you want to send translations to the user
# you don't want to show the current browser language in list of possible languages for translation
def removeLanguage(languages, code):
    for i in languages:
        if i.code == code:
            languages.remove(i)
            break
    return languages


# Prepares the translation dictionary
# This gets all the current translations from request
def getTranslationDict(request, languages):
    translation = {}
    for lang in languages:
        translation[lang] = {}
        for obj in request.POST:
            if lang.name in obj:
                name = obj.replace(lang.name + "_", "")
                translation[lang][name] = request.POST.get(obj)

    return translation


# Adds subjects to a newly created list
def addSubjectsTo(list, request):
    max_subjects = int(request.POST.get("subjects_amount"))
    if max_subjects == 0:
        list.addSubject("")
    for i in range(max_subjects):
        subj = request.POST.get("subject" + str(i))
        if subj is not None:
            list.addSubject(subj)


# The view for createExerciseList.html
@require_login
def createExerciseList(request):
    browser_lang = getBrowserLanguage(request)
    # Prepare info
    prog_languages = object_manager.allProgrammingLanguages()
    languages = removeLanguage(object_manager.getAllLanguages(), browser_lang.code)

    # If there is a POST request to handle
    if request.method == 'POST':
        list_name = request.POST.get('list_name', '')
        list_description = request.POST.get('description_text', '')
        difficulty = request.POST.get('difficulty', '')
        prog_lang = request.POST.get('prog_lang', '')

        user = logged_user(request)
        translation = getTranslationDict(request, languages)

        exlist_id = object_manager.insertExerciseList(list_name, list_description, int(difficulty), user.id,
                                                      str(time.strftime("%Y-%m-%d %H:%M:%S")), prog_lang,
                                                      browser_lang.id, translation)
        # get subjects
        exercise_list = object_manager.createExerciseList(exlist_id, browser_lang.id)
        addSubjectsTo(exercise_list, request)
        # Update user's points for badges
        user.createdExerciseList()
        return HttpResponse("/l/" + str(exlist_id))

    return render(request, 'createExerciseList.html', {"prog_languages": prog_languages, "languages": languages})

# Update subjects when editing a list
def updateSubjects(list, subjects, request):
    updated_subjects_amount = int(request.POST.get("subjects_amount"))
    updated_subjects = []
    for i in range(updated_subjects_amount):
        subject = request.POST.get('subject' + str(i))
        if subject is not None:
            updated_subjects.append(subject)

    removed_subjects = set(subjects) - set(updated_subjects)
    intersection = set(subjects) & set(updated_subjects)
    subjects_to_add = set(updated_subjects) - intersection

    for subject in removed_subjects:
        list.deleteSubject(subject)

    for subject in subjects_to_add:
        list.addSubject(subject)

    return updated_subjects

# The view for editList.html
@require_login
def editList(request, listId):
    browser_lang = getBrowserLanguage(request)
    exercise_list = object_manager.createExerciseList(listId, browser_lang.id)
    user = logged_user(request)
    # Remove browser language from available languages
    languages = removeLanguage(object_manager.getAllLanguages(), browser_lang.code)
    # Check if list exists
    if exercise_list is None or exercise_list.created_by != user.id:
        return redirect('/')
    subjects = exercise_list.allSubjects()
    prog_langs = object_manager.allProgrammingLanguages()

    if request.method == 'POST':
        # Get updated information
        updated_list_name = request.POST.get('list_name')
        updated_difficulty = request.POST.get('difficulty')

        updated_prog_lang = request.POST.get('prog_lang', '')
        updated_description = request.POST.get('description_text')
        new_order = request.POST.get('order')
        # Reorder our exercises if necessary
        new_order = filterOrder(new_order)
        exercise_list.reorderExercises(new_order, browser_lang.code)

        subjects = updateSubjects(exercise_list, subjects, request)

        translation = getTranslationDict(request, languages)
        # set current browser translation
        translation[browser_lang] = {"name": updated_list_name, "description": updated_description}

        exercise_list.update(updated_list_name, updated_description, updated_difficulty,
                             object_manager.getProgrLanguageObject(updated_prog_lang), translation)

    all_exercises = exercise_list.allExercises(browser_lang.code)
    current_translations = exercise_list.getAllTranslations()

    return render(request, 'createExerciseList.html', {'list': exercise_list,
                                                       'subjects': subjects,
                                                       'prog_languages': prog_langs,
                                                       'all_exercises': all_exercises,
                                                       'languages': languages,
                                                       'translations': current_translations,
                                                       'edit': True})


# get multiple choice information when creating new exercise
def getMultipleChoiceInfo(request, exercise_max_score):
    answer = []
    for i in range(exercise_max_score + 1):
        cur_answer = request.POST.get("answer" + str(i), "")
        if cur_answer != "":
            answer.append(cur_answer)

    exercise_answer = answer
    correct_answer = request.POST.get("correct_answer")
    exercise_penalty = 3
    return exercise_answer, correct_answer, exercise_penalty


# Get code information when creating new exercise
def getCodeInfo(request, exercise_max_score):
    hints = []
    exercise_answer = [request.POST.get("output")]

    for j in range(1, exercise_max_score + 1):
        cur_hint = request.POST.get("hint" + str(j), "")
        if cur_hint != "":
            hints.append(cur_hint)

    return exercise_answer, hints


# The view for createExercise.html
@require_login
def createExercise(request, listId=0):
    browser_lang = getBrowserLanguage(request)
    exercise_list = object_manager.createExerciseList(listId, browser_lang.id)
    user = logged_user(request)
    languages = removeLanguage(object_manager.getAllLanguages(), browser_lang.code)

    if request.method == 'POST':
        # Get information
        translation = getTranslationDict(request, languages)
        exercise_penalty = 1
        exercise_question_text = request.POST.get('Question')
        exercise_type = request.POST.get('exercise_type')
        if exercise_type == "Multiple choice":
            exercise_type = "Open Question"

        hints = []
        exercise_title = request.POST.get('title')
        exercise_number = exercise_list.getLastExercise() + 1
        exercise_question = Question(exercise_question_text, browser_lang.code)
        exercise_answer = None
        correct_answer = 1

        code = request.POST.get('code', '')
        exercise_max_score = int(request.POST.get('max', '1'))

        # Get the according information for each exercise_type
        if exercise_type == 'Open Question':
            exercise_answer, correct_answer, exercise_penalty = getMultipleChoiceInfo(request, exercise_max_score)

        # Turtle or Code
        else:
            exercise_answer, hints = getCodeInfo(request, exercise_max_score)

        exercise_list.insertExercise(exercise_max_score, exercise_penalty, exercise_type, user.id,
                                     str(time.strftime("%Y-%m-%d %H:%M:%S")), exercise_number, exercise_question,
                                     exercise_answer, correct_answer, hints, browser_lang, exercise_title, translation,
                                     code)
        return redirect("/l/" + str(listId))

    if exercise_list:
        if exercise_list.created_by != user.id:
            return redirect('/')
        else:
            return render(request, 'createExercise.html', {'edit': False,
                                                           'list': exercise_list,
                                                           'languages': languages})

    return redirect('/')


# Function to filter the new order of the exercises.
def filterOrder(order):
    if len(order) == 0:
        return []

    new_order = []
    splitted = order.split(',')
    for i in splitted:
        new_order.append(int(i.replace('exercise', '')))
    return new_order


# Edit an openQuestion (Multiple choice)
def editOpenQuestion(exercise, request):
    exercise_answer = []
    for i in range(exercise.max_score + 1):
        cur_answer = request.POST.get("answer" + str(i), "")
        if cur_answer != "":
            exercise_answer.append(cur_answer)

    exercise.penalty = 3
    correct_answer = request.POST.get("correct_answer")
    return exercise_answer, correct_answer


# Edit a codeQuestion
def editCodeQuestion(exercise, request):
    hints = []
    exercise_answer = [request.POST.get("output")]
    exercise.penalty = 1
    for j in range(1, exercise.max_score + 1):
        cur_hint = request.POST.get("hint" + str(j), "")
        if cur_hint != "":
            hints.append(cur_hint)

    return exercise_answer, hints


# Function to update an exercise after a post request on the edit exercise page
def handleEditExercisePost(exercise_id, browser_lang, listId, exercise_number, languages, request):
    # get information
    exercise = object_manager.createExercise(exercise_id, browser_lang.code)
    exercise.question = request.POST.get('Question')
    exercise.title = request.POST.get('title')
    exercise.exerciseList_id = int(listId)
    exercise.exercise_number = int(exercise_number)
    exercise.exercise_type = request.POST.get('exercise_type')
    hints = []
    exercise.code = request.POST.get('code', '')
    exercise.max_score = int(request.POST.get('max', '1'))
    exercise_answer = None
    correct_answer = 1

    # Update our question type
    if exercise.exercise_type == 'Open Question':
        exercise_answer, correct_answer = editOpenQuestion(exercise, request)
    else:
        exercise_answer, hints = editCodeQuestion(exercise, request)

    # Get the translation dictionary from our request
    translation = getTranslationDict(request, languages)

    exercise.update(correct_answer, exercise_answer, hints, browser_lang, translation, user.id)


@require_login
# view for editing an exercise
def editExercise(request, listId, exercise_id, exercise_number):
    user = logged_user(request)
    # list_id is required, if someone copies our exercise in an other list we want to know in which list we are
    browser_lang = getBrowserLanguage(request)
    exercise_list = object_manager.createExerciseList(listId, browser_lang.id)
    languages = removeLanguage(object_manager.getAllLanguages(), browser_lang.code)

    if request.method == 'POST':
        handleEditExercisePost(exercise_id, browser_lang, listId, exercise_number, languages, request)
        return redirect("/l/" + str(listId))

    if exercise_list and user.id == exercise_list.created_by:
        # Extra check so you can't just surf to the url and edit the exercise
        exercise = object_manager.createExercise(exercise_id, browser_lang.code)
        all_answers = exercise.allAnswers()
        expected_code_answer = ""
        if exercise.exercise_type == 'Code' or exercise.exercise_type == 'Turtle':
            for i, ans in enumerate(all_answers):
                if i == exercise.correct_answer - 1:
                    expected_code_answer = ans
                    break

        all_hints = exercise.allHints()
        amount_hints = 0
        if all_hints is not None:
            amount_hints = len(all_hints)
        translation = exercise.getTranslations(languages)

        return render(request, 'createExercise.html', {'edit': True,
                                                       'exercise': exercise,
                                                       'all_answers': all_answers,
                                                       'expected_code_answer': expected_code_answer,
                                                       'all_hints': all_hints,
                                                       'am_hints': amount_hints,
                                                       'list': exercise_list,
                                                       'languages': languages,
                                                       'translations': json.dumps(translation)})

# Generate the html for the import modal view
def createImportHTML(all_lists, all_exercises):
    html = ""
    for list in all_lists:

        html += """<li class=\"accordion-navigation\">
            <a href="#Exerc{list_id}">{list_name}</a>
            <div id="Exerc{list_id}" class="content">
            <div class="row">
            <div class="large-centered columns">
            <table>
            <thead>
            <tr>
            <th width="200">Title</th>
            <th width="150">copy original</th>
            <th width="150">reference</th>
            </tr>
            </thead>""".format(list_id=list.id, list_name=list.name)
        for exercise in all_exercises[list.id]:
            html += """<tbody>
                <td>{title}</td>
                <td><input id="checkbox_copy{id}" name="checkbox_copy{id}" type="checkbox"></td>
                <td><input id="checkbox_import{id}" name="checkbox_import{id}" type="checkbox"></td>
                </tbody>""".format(title=exercise.title, id=exercise.id)

        html += """</table>
                </div>
                </div>
                </div>
                </li>"""
    return html


# Import exercise view
@require_login
def importExercise(request, listId):
    browser_lang = getBrowserLanguage(request)
    exercise_list = object_manager.createExerciseList(listId, browser_lang.id)
    if exercise_list and exercise_list.created_by == logged_user(request).id:
        # The only user who can import something into a list, is the creator of that list

        # Get all the lists
        all_lists_id = object_manager.getExerciseListsOnProgLang(exercise_list.programming_language.name)
        if request.method == "GET" and request.GET:
            all_lists_id = object_manager.filterImportsLists(request.GET['search_input'])

        all_lists = []
        for i in all_lists_id:
            all_lists.append(object_manager.createExerciseList(i, browser_lang.id))

        # Get all the exercises for each list
        # Store them as list id, exercises pair
        all_exercises = {}
        for i in all_lists:
            all_exercises[i.id] = i.allExercises(browser_lang.code)

        if request.method == "GET" and request.GET:
            return HttpResponse(createImportHTML(all_lists, all_exercises))

        if request.method == "POST":
            # Check which exercises to copy/import
            copies = []
            references = []
            for key, i in all_exercises.items():
                for ex in i:
                    copy = request.POST.get('checkbox_copy/' + str(key) + '/' + str(ex.exercise_number))
                    ref = request.POST.get('checkbox_import/' + str(key) + '/' + str(ex.exercise_number))
                    if copy is not None:
                        copies.append(ex)

                    if ref is not None:
                        references.append(ex)

            for ref in references:
                exercise_list.insertExerciseByReference(ref.id)
            for copy in copies:
                exercise_list.copyExercise(copy.id)

        return render(request, 'importExercise.html', {'all_lists': all_lists,
                                                       'all_exercises': all_exercises,
                                                       'list_id': listId})

    return redirect('/')


# Rounds integers or tells the user is the givn object was None
def InvalidOrRound(object):
    if object is None:
        object = "N/A"
    else:
        object = round(object)
    return object


def importOnList(exercise_list, browser_lang, user, request):
    # just to be sure we can't import stuff in our own list
    # Import parts of list
    all_exercises = exercise_list.allExercises(browser_lang.code)
    copies = []
    references = []
    for i in all_exercises:
        copy = request.POST.get('checkbox_copy' + str(i.exercise_number))
        ref = request.POST.get('checkbox_import' + str(i.exercise_number))
        if copy is not None:
            copies.append(i)

        if ref is not None:
            references.append(i)
    # Here we got the exercises
    # Check in which lists we need to insert them
    mylists = user.getUserLists(browser_lang.id)
    lists = []
    for l in mylists:
        found = request.POST.get('mylist_' + str(l.id))
        if found:
            for ref in references:
                l.insertExerciseByReference(ref.id)
            for copy in copies:
                l.copyExercise(copy.id)


# Getter for recommended lists for a user
def recommendLists(user, browser_lang, exercise_list):
    similar_lists = []
    similar_list_ids = []
    # For the recommended lists, we'll first check if the user solved the current list
    if exercise_list:
        made_list = user.getMadeList(exercise_list.id, browser_lang.id)
        if made_list:
            similar_list_ids = recommendNextExerciseLists(made_list, user)
        else:
            similar_list_ids = listsLikeThisOne(exercise_list.id, user)
    for list_id in similar_list_ids:
        similar_lists.append(object_manager.createExerciseList(list_id, browser_lang.id))

    return similar_lists

# Check if the list has been shared, if the user i the owner and which of the exercises have been completed yet
def DecidesharedOwnerAllExWithScore(all_exercises, user, exercise_list, id):
    shared_result = True
    list_owner = False
    all_exercises_with_score = []
    if user:
        shared_result = user.sharedResult(exercise_list.id)
        for exercise in all_exercises:
            completed = object_manager.getInfoForUserForExercise(user.id, id, exercise.exercise_number)
            if completed is not None:
                if completed['solved'] == 1:
                    exercise.solved = True
                    all_exercises_with_score.append((exercise, completed['exercise_score']))
                else:
                    all_exercises_with_score.append((exercise, None))
            else:
                all_exercises_with_score.append((exercise, None))

        list_owner = (user.id == exercise_list.created_by)
    else:
        all_exercises_with_score = [(x, None) for x in all_exercises]
    return shared_result, list_owner, all_exercises_with_score

# Calculate score of user on list
def getPercentage(all_exercises, list_owner):
    cur_exercise = 0
    percent = 0
    solved_all = False
    found = False

    if list_owner:
        if all_exercises:
            cur_exercise = all_exercises[0].exercise_number
        else:
            cur_exercise = 1
    else:
        if len(all_exercises) > 0:
            cur_exercise = all_exercises[0].exercise_number

        # For all exercises we've made increase our percent counter
        for e in all_exercises:
            if e.solved:
                found = True
                percent += 1
                if cur_exercise < e.exercise_number:
                    cur_exercise = e.exercise_number

        if len(all_exercises) < percent:
            found = False
            cur_exercise = all_exercises[0].exercise_number

        elif percent > 0 and len(all_exercises) > percent:
            cur_exercise = all_exercises[percent].exercise_number

        if len(all_exercises) > 0:
            percent = percent / len(all_exercises) * 100
            if percent > 100:
                percent = 100

        if percent == 100:
            solved_all = True

    return percent, solved_all, found, cur_exercise


# The view for createExercise.html
def list(request, id=0):
    user = logged_user(request)
    browser_lang = getBrowserLanguage(request)
    exercise_list = object_manager.createExerciseList(id, browser_lang.id)
    # Check if list exists
    if exercise_list is None:
        return redirect('/')

    # Statistic info about this list
    avg_score = InvalidOrRound(exercise_list.averageOfUsersForThisList())
    avg_rating = InvalidOrRound(exercise_list.averageRatingOfUsersForThisList())
    number_of_users = InvalidOrRound(exercise_list.amountOfUsersWhoMadeThisList())
    user_score = 0
    user_date = None

    # Other general info about the list
    subjects = exercise_list.allSubjects()
    creator = exercise_list.creator()
    created_on = exercise_list.created_on

    if subjects is None:
        subjects = []

    # if the user interacts with the page (POST request is sent)
    if request.method == 'POST':
        # User gives a rating to our page
        if request.POST.get('rating') is not None and user is not None:
            user.ratedExerciseList()
            user.updateListRating(exercise_list.id, int(request.POST.get('rating')))
            avg_rating = InvalidOrRound(exercise_list.averageRatingOfUsersForThisList())
            return HttpResponse(avg_rating)

        elif 'share_result' in request.POST:
            user.shareExerciseListResult(exercise_list.id)

        elif user is not None and user.id != exercise_list.created_by:
            importOnList(exercise_list, browser_lang, user, request)

    if exercise_list:
        all_exercises = exercise_list.allExercises(browser_lang.code)
        if user:
            personal_list = user.getMadeList(exercise_list.id, browser_lang.id)
            if personal_list:
                user_score = personal_list.score
                user_date = personal_list.made_on

        all_exercises_with_score = []
        shared_result = True
        list_owner = False
        shared_result, list_owner, all_exercises_with_score = DecidesharedOwnerAllExWithScore(all_exercises, user, exercise_list, id)

        # Calculate percentage for this list (score of user)
        percent, solved_all, found, cur_exercise = getPercentage(all_exercises, list_owner)

        # Lists like this one
        similar_lists = []
        user_rating = 0
        user_lists = None
        if user:
            user_lists = user.getUserLists(browser_lang.id)
            user_rating = user.getRatingForList(exercise_list.id)
            similar_lists = recommendLists(user, browser_lang, exercise_list)

        return render(request, 'list.html', {'list_owner': list_owner,
                                             'id': exercise_list.id,
                                             'all_exercises': all_exercises_with_score,
                                             'subjects': subjects,
                                             'avg_score': avg_score,
                                             'avg_rating': avg_rating,
                                             'number_of_users': number_of_users,
                                             'found': found,
                                             'cur_exercise': cur_exercise,
                                             'percent': int(percent),
                                             'solved_all': solved_all,
                                             'user_rating': user_rating,
                                             'creator': creator,
                                             'created_on': created_on,
                                             'similar_lists': similar_lists,
                                             'list': exercise_list,
                                             'user_lists': user_lists,
                                             'user_score': user_score,
                                             'user_date': user_date,
                                             'shared_result': shared_result,
                                             'user': user})
    else:
        return redirect('/')


# Restores the question where the user left off
def restoreQuestion(all_exercise, exercise_number, current_user, list_id):
    current_exercise = None
    current_score = None
    last_hint_used = None
    current_answer = None
    correct_answer = None

    for i in all_exercise:
        if i.exercise_number == int(exercise_number):
            current_exercise = i
            if current_exercise.exercise_type == 'Open Question':
                correct_answer = current_exercise.correct_answer
            elif current_exercise.exercise_type == 'Code':
                correct_answer = stripStr(current_exercise.allAnswers()[0])
            else:
                answer_data = json.loads(str(current_exercise.allAnswers()[0]))
                correct_answer = [str(answer_data["points"]), str(answer_data["edges"])]

            info = None
            if current_user:
                info = object_manager.getInfoForUserForExercise(current_user.id, list_id, exercise_number)
                last_hint_used = current_user.latestHintIUsedForExercise(list_id, exercise_number)
                current_answer = current_user.getLastAnswerForExercise(list_id, exercise_number)
            penalty = current_exercise.penalty
            if info:
                current_score = info['exercise_score']

            if not current_score:
                current_score = current_exercise.max_score
            if current_exercise.exercise_type == 'Open Question':
                current_answer = int(current_answer)
            break

    return current_exercise, current_score, last_hint_used, current_answer, correct_answer


# View for answering a question/exercise
def answerQuestion(request, list_id, exercise_number):
    current_user = logged_user(request)
    if request.method == "POST":
        # If user submits a post request, then we need to go to the submit page!
        return redirect('/l/' + list_id + '/' + exercise_number + '/submit')

    list_owner = False
    browser_lang = getBrowserLanguage(request)
    exercise_list = object_manager.createExerciseList(list_id, browser_lang.id)
    current_answer = None
    correct_answer = ""
    last_hint_used = 0
    solved = None

    if current_user:
        # Check if we've solved this exercise already
        solved = current_user.haveISolvedExercise(exercise_list.id, exercise_number)
    if exercise_list:

        all_exercise = exercise_list.allExercises(browser_lang.code)

        # Restore our progress
        progress = restoreQuestion(all_exercise, exercise_number, current_user, list_id)

        current_exercise = progress[0]
        current_score = progress[1]
        last_hint_used = progress[2]
        current_answer = progress[3]
        correct_answer = progress[4]

        if current_exercise:
            list_owner = False
            if current_user:
                list_owner = (current_user.id == exercise_list.created_by)
            return render(request, 'answerQuestion.html', {"exercise": current_exercise,
                                                           "answers": current_exercise.allAnswers(),
                                                           "list_id": list_id,
                                                           "hints": current_exercise.allHints(),
                                                           "current_answer": current_answer,
                                                           "solved": solved,
                                                           "last_hint_used": last_hint_used,
                                                           "current_score": current_score,
                                                           "penalty": current_exercise.penalty,
                                                           'list_owner': list_owner,
                                                           'correct_answer': correct_answer})

        # If the exercise doesn't exist, redirect to the list page
        else:
            return redirect('/l/' + list_id)
    # Redirect to home if exercise list does't exist
    return redirect('/')


# Strips string from \n or \r
def stripStr(string):
    strip = ["\n", "\r"]
    s = string
    for i in strip:
        s = s.replace(i, "")
    return s


def returnScore(current_score):
    if current_score < 0:
        return 0
    return current_score

# User requesting a hint
@require_login
def addHint(request):
    exercise_number = int(request.POST.get('ex_number'))
    list_id = int(request.POST.get('list_id'))
    amount_of_hints = int(request.POST.get('amount_of_hints'))
    max_score = int(request.POST.get('max_score'))
    penalty = int(request.POST.get('penalty'))
    user = logged_user(request)
    user.useHintForExercise(list_id, exercise_number, amount_of_hints, max_score, penalty)
    return HttpResponse('Everything went fine')

# Check if a user finished the list
def checkMadeList(exercise_list, browser_lang, all_exercise, user):
    user_made_all = True
    users_exercises = exercise_list.getAllExercForUserForList(user.id)
    for ex_info in users_exercises:
        if not ex_info['solved']:
            user_made_all = False
    if user_made_all:
        if len(users_exercises) == len(all_exercise):
            list_score = 0
            max_list_score = 0
            for ex in users_exercises:
                list_score += ex['exercise_score']
                max_list_score += ex['max_score']
            list_score = list_score * 100
            list_score = list_score / max_list_score
            user.madeList(exercise_list.id, list_score, 0)
            challenge_manager.checkActiveChallenges(user.id, browser_lang.id)
            return True

    return False
# Check if the user gave a correct answer
def checkCorrectAnswer(current_exercise, user_output, request, current_score, user):
    user_code = request.POST.get('user_code', '')
    hint = request.POST.get("used_hints")
    penalty = current_exercise.penalty
    exercise_number = current_exercise.exercise_number
    list_id = current_exercise.exerciseList_id
    solved = False
    if current_exercise.exercise_type == 'Open Question':
        selected_answer = request.POST.get('corr_answer')

        if current_exercise.correct_answer == int(selected_answer):
            # Woohoo right answer!
            solved = True
            current_score = returnScore(current_score)

            object_manager.userMadeExercise(user.id, current_score, 1, str(time.strftime("%Y-%m-%d %H:%M:%S")),
                                            int(list_id), int(exercise_number), selected_answer, hint)
        else:
            current_score = returnScore(current_score - penalty)
            # Even though we didn't complete this exercise, we need to remember the progress of the user
            object_manager.userMadeExercise(user.id, current_score, 0, str(time.strftime("%Y-%m-%d %H:%M:%S")),
                                            int(list_id), int(exercise_number), selected_answer, hint)

    elif current_exercise.exercise_type == 'Code' or current_exercise.exercise_type == 'Turtle':
        # For code you only have one answer so lets get it
        correct_answer = stripStr(current_exercise.allAnswers()[0])
        user_output = stripStr(user_output)

        if correct_answer == user_output or (
                correct_answer == '*' and user_output != '') or user_output == "~~success~~":
            current_score = returnScore(current_score)
            solved = True
            object_manager.userMadeExercise(user.id, current_score, 1, str(time.strftime("%Y-%m-%d %H:%M:%S")),
                                            int(list_id), int(exercise_number), user_code, hint)

        else:
            # We didn't get the right answer! Deduct points!
            current_score = returnScore(current_score - penalty)
            object_manager.userMadeExercise(user.id, current_score, 0, str(time.strftime("%Y-%m-%d %H:%M:%S")),
                                            int(list_id), int(exercise_number), user_code, hint)

    return solved, current_score
# The view when the users submits his/her answer
@require_login
def submit(request, list_id, exercise_number):
    user = logged_user(request)
    exercise_number = int(exercise_number)
    browser_lang = getBrowserLanguage(request)
    exercise_list = object_manager.createExerciseList(list_id, browser_lang.id)
    if exercise_list:
        # Get the correct exercise
        solved = False
        all_exercise = exercise_list.allExercises(browser_lang.code)
        current_exercise = None
        for i in all_exercise:
            if i.exercise_number == exercise_number:
                current_exercise = i
                break

        if current_exercise is None:
            return redirect('/')

        if request.method == 'POST':
            # Check which button has been pressed
            if 'b_tryagain' in request.POST:
                # Redirect to the same exercise
                return redirect('/l/' + list_id + '/' + str(exercise_number))
            elif 'b_returntolist' in request.POST:
                return redirect('/l/' + list_id)
            elif 'b_nextexercise' in request.POST:
                # Redirects to next exercise
                if len(all_exercise) < exercise_number + 1:
                    user.solvedExerciseList(exercise_list.created_by)
                    return redirect('/l/' + list_id + '/')
                else:
                    return redirect('/l/' + list_id + '/' + str(exercise_number + 1))

            info = object_manager.getInfoForUserForExercise(user.id, list_id, exercise_number)
            current_score = None
            if info is not None:
                current_score = object_manager.getScoreForExerciseForUser(user.id, list_id, exercise_number)

            # So the user hasn't made this exercise yet
            if current_score is None:
                current_score = current_exercise.max_score

            max_score = current_exercise.max_score
            user_output = request.POST.get('code_output', '')

            # Check if the user gave a correct answer
            solved, current_score = checkCorrectAnswer(current_exercise, user_output, request, current_score, user)

        next_exercise = exercise_number + 1

        # Checking if user made list
        if checkMadeList(exercise_list, browser_lang, all_exercise, user):
            next_exercise = 0

        return render(request, 'submit.html', {"solved": solved,
                                               "list_id": list_id,
                                               "current_score": current_score,
                                               "max_score": max_score,
                                               "question_type": current_exercise.exercise_type,
                                               "user_output": user_output,
                                               "next_exercise": next_exercise})

    else:
        return redirect('/')

# Generate HTML for list planets
def createListElem(i, elem):
    class_name = "planet "
    if elem.programming_language.id == 1:
        class_name += "python"
    elif elem.programming_language.id == 2:
        class_name += "cpp"
    elif elem.programming_language.id == 3:
        class_name += "sql"

    subjects = " | "
    for subj in elem.allSubjects():
        subjects = subjects + subj + " | "

    planet_info = """<div class="large-4 columns large-centered list_info">
        <div class=\"information panel radius\" id="info{for_i}" hidden="True">
          <div class=\"row\">
            <div class=\"text-center\">
              <b>{list_name}</b>
            </div>
          </div>
          <br>
          <div class=\"row\">
            <div class=\"text-center\">
              <b>Difficulty:</b> {list_difficulty}
            </div>
          </div>
          <div class=\"row\">
            <div class=\"text-center\">
              <b>Created by:</b> {list_creator}
            </div>
          </div>
          <div class=\"row\">
            <div class=\"text-center\">
              <b>Exercises:</b> {list_amountOfExercises}
            </div>
          </div>
          <div class=\"row\">
            <div class=\"text-center\">
              <b>Subjects:</b>""" + subjects + """
            </div>
          </div>
          <div class=\"row\">
            <div class=\"text-center\">
              <a class=\"round tiny button\" type=\"button\" href=\"/l/{list_id}\">Explore!</a>
            </div>
          </div>
         </div>
        </div>"""

    pi_format = planet_info.format(list_name=elem.name, list_difficulty=elem.difficulty,
                                   list_creator=elem.creator().name(), list_amountOfExercises=elem.amountOfExercises(),
                                   list_id=elem.id, for_i=i + 1)

    return (
        """<div><div class=\"{class_name}\">{for_i}</div></div>""".format(class_name=class_name, for_i=i + 1),
        pi_format)

# Charts for lists
def createChartsForOverview():
    # Amount of lists per programming language
    lists_per_prog_lang = statistics_analyzer.AmountOfExerciseListsPerProgrammingLanguage()
    pie_chart = graph_manager.makePieChart('colours', 180, 100,
                                           graphmanager.color_tuples,
                                           lists_per_prog_lang['labels'],
                                           lists_per_prog_lang['data'], _('Planets/Programming Language'))
    # Amount of subjects:
    # Colors
    color_info1 = graphmanager.ColorInfo("#f04124", "#f04124", "#f76148", "#f76148")
    color_info2 = graphmanager.ColorInfo("#FF9437", "#FF9437", "#ffa85d", "#ffa85d")

    # Data
    most_popular_subjects = statistics_analyzer.mostPopularSubjectsTopX(5)
    bar_chart = graph_manager.makeBarChart('subjectsgraph', 200, 200,
                                           [color_info2, color_info1], most_popular_subjects['labels'],
                                           most_popular_subjects['data'], ["subject"], False,
                                           _('Most Popular Subjects'))
    # Users with most made lists
    users_with_mosts_made_lists = statistics_analyzer.mostExerciseListsTopX(5)
    bar_chart2 = graph_manager.makeBarChart('activeusers', 200, 200, [color_info1, color_info2],
                                            users_with_mosts_made_lists['labels'], users_with_mosts_made_lists['data'],
                                            ["#exercises"], False, _('Users who made the most lists'))

    return pie_chart, bar_chart, bar_chart2


# View for listoverview
def listOverview(request):
    pie_chart, bar_chart, bar_chart2 = createChartsForOverview()

    browser_lang = getBrowserLanguage(request)
    list_name = '%'
    min_list_difficulty = 1
    max_list_difficulty = 5
    user_first_name = '%'
    user_last_name = '%'
    prog_lang_name = '%'
    order_mode = "ASC"
    subject_name = '%'

    if request.method == "POST" and request.is_ajax():
        list_name = request.POST.get('title', '%')
        min_list_difficulty = int(request.POST.get('min_difficulty', 1))
        max_list_difficulty = int(request.POST.get('max_difficulty', 5))
        prog_lang_name = request.POST.get('prog_lang')
        if prog_lang_name == '':
            prog_lang_name = '%'

        user_name = request.POST.get('user')
        if user_name != "":
            user_name = user_name.split(' ')
            user_first_name = user_name[0]
            if len(user_name) > 1:
                user_last_name = user_name[1]

        subjects = request.POST.get('subjects')
        if subjects != "":
            subject_name = subjects.split(',')

        order_mode = request.POST.get('order_mode')
        if order_mode == "Ascending":
            order_mode = "ASC"
        else:
            order_mode = "DESC"

        all_lists = object_manager.filterOn(list_name, min_list_difficulty, max_list_difficulty, user_first_name,
                                            user_last_name, prog_lang_name, subject_name, order_mode, browser_lang.id)
        html = ""
        info = ""
        for i, obj in enumerate(reversed(all_lists)):
            obj.created_on = obj.created_on.strftime("%Y-%m-%d %H:%M:%S")
            h, i = createListElem(i, obj)
            html += h
            info += i

        return HttpResponse(json.dumps({"planets": html, "info": info}))

    all_lists = reversed(
        object_manager.filterOn(list_name, min_list_difficulty, max_list_difficulty, user_first_name, user_last_name,
                                prog_lang_name, subject_name, order_mode, browser_lang.id))

    return render(request, 'listOverview.html', {"all_lists": all_lists,
                                                 "languages": object_manager.allProgrammingLanguages(),
                                                 'lists_per_prog_lang_graph': pie_chart,
                                                 'most_popular_subjects': bar_chart,
                                                 'users_with_mosts_made_lists':
                                                     bar_chart2})
