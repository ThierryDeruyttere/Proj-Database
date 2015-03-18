from django.shortcuts import render, redirect

import time
import json

from managers.om import *
from managers.gm import *
from codegalaxy.authentication import require_login, logged_user
from managers.om.exercise import Question
from pymysql import escape_string
from django.http import HttpResponse

object_manager = objectmanager.ObjectManager()
statistics_analyzer = statisticsanalyzer.StatisticsAnalyzer()
graph_manager = graphmanager.GraphManager()

@require_login
def createExerciseList(request):
    languages = object_manager.allProgrammingLanguages()
    if request.method == 'POST':
        list_name = request.POST.get('list_name', '')
        list_description = request.POST.get('description_text', '')
        difficulty = request.POST.get('difficulty', '')
        prog_lang = request.POST.get('prog_lang', '')
        user = logged_user(request)
        exlist_id = object_manager.insertExerciseList(list_name, list_description, int(difficulty), user.id, str(time.strftime("%Y-%m-%d")), prog_lang)
        # get subjects
        current_subject = 0
        exercise_list = object_manager.createExerciseList(exlist_id)

        while(request.POST.get("subject" + str(current_subject)) is not None):
            exercise_list.addSubject(request.POST.get("subject" + str(current_subject)))
            current_subject += 1

        return redirect("/l/" + str(exlist_id))

    return render(request, 'createExerciseList.html', {"languages": languages})


def InvalidOrRound(object):
    if object is None:
        object = "N/A"
    else:
        object = round(object)
    return object

def list(request, id=0):
    exercise_list = object_manager.createExerciseList(id)
    #FIRST CHECK IF LIST EXISTS BEFORE DOING ANYTHING
    if exercise_list is None:
        return redirect('/')

    avg_score = InvalidOrRound(exercise_list.averageOfUsersForThisList())
    avg_rating = InvalidOrRound(exercise_list.averageRatingOfUsersForThisList())
    number_of_users = InvalidOrRound(exercise_list.amountOfUsersWhoMadeThisList())

    subjects = exercise_list.allSubjects()
    languages = object_manager.allProgrammingLanguages()
    current_language = exercise_list.programming_language_string

    if subjects is None:
        subjects = []

    if request.method == 'POST':
        updated_list_name = request.POST.get('updated_list_name')
        updated_difficulty = request.POST.get('updated_difficulty')
        updated_subjects_amount = int(request.POST.get('current_subjects'))
        updated_subjects = []
        updated_prog_lang = request.POST.get('prog_lang', '')
        updated_description = request.POST.get('updated_description_text')

        for i in range(updated_subjects_amount):
            subject = request.POST.get('subject' + str(i))
            if subject is not None:
                updated_subjects.append(subject)

        removed_subjects = set(subjects) - set(updated_subjects)
        intersection = set(subjects) & set(updated_subjects)
        subjects_to_add = set(updated_subjects) - intersection

        for subject in removed_subjects:
            exercise_list.deleteSubject(subject)

        for subject in subjects_to_add:
            exercise_list.addSubject(subject)

        exercise_list.update(updated_list_name, updated_description, updated_difficulty, updated_prog_lang)

    if exercise_list:
        prog_lang = exercise_list.programming_language_string
        all_exercises = exercise_list.allExercises("en")

        correct_user = False
        if logged_user(request):
            for exercise in all_exercises:
                print(object_manager.getInfoForUserForExercise(logged_user(request).id, exercise.id))
                if object_manager.getInfoForUserForExercise(logged_user(request).id, exercise.id):
                    exercise.solved = True

            correct_user = (logged_user(request).id == exercise_list.created_by)

        found = False
        cur_exercise = 0
        if len(all_exercises) > 0:
            cur_exercise = all_exercises[0].id

        percent = 0
        for e in all_exercises:
            if e.solved:
                found = True
                percent+=1
                if cur_exercise < e.id:
                    cur_exercise = e.id


        if len(all_exercises) < percent:
            found = False
            cur_exercise = all_exercises[0].id
        elif percent > 0 and len(all_exercises) > percent :
                cur_exercise = all_exercises[percent].id

        if len(all_exercises) > 0:
            percent = percent/len(all_exercises) * 100
            if percent > 100:
                percent = 100

        return render(request, 'list.html', {'list_name': exercise_list.name,
                                             'list_description': exercise_list.description,
                                             'list_difficulty': exercise_list.difficulty,
                                             'list_programming_lang': prog_lang,
                                             'correct_user': correct_user,
                                             'id': exercise_list.id,
                                             'all_exercises': all_exercises,
                                             'subjects': subjects,
                                             'programming_languages': languages,
                                             'current_prog_lang': current_language,
                                             'avg_score': avg_score,
                                             'avg_rating': avg_rating,
                                             'number_of_users': number_of_users,
                                             'found': found,
                                             'cur_exercise': cur_exercise,
                                             'percent': percent})
    else:
        return redirect('/')

@require_login
def createExercise(request, listId=0):
    exercise_list = object_manager.createExerciseList(listId)
    user = logged_user(request)
    if request.method == 'POST':
        exercise_difficulty = int(request.POST.get('difficulty'))
        exercise_penalty = 1
        exercise_question_text = request.POST.get('Question')
        exercise_type = request.POST.get('exercise_type')
        hints = []
        exercise_title = request.POST.get('title')

        exercise_number = exercise_list.getLastExercise() + 1

        exercise_question = Question(exercise_question_text, 1)
        exercise_answer = None
        correct_answer = 1

        code = request.POST.get('code', '')
        exercise_max_score = int(request.POST.get('max', '1'))

        if(exercise_type == 'Open Question'):
            answer = []
            for i in range(1, exercise_max_score + 1):
                cur_answer = request.POST.get("answer" + str(i), "")
                if cur_answer != "":
                    answer.append(escape_string(cur_answer))

            exercise_answer = answer
            correct_answer = request.POST.get("correct_answer")
            exercise_penalty = 3

        else:
            expected_answer = request.POST.get("output")
            exercise_answer = [expected_answer]

            for j in range(1, exercise_max_score + 1):
                cur_hint = request.POST.get("hint" + str(j), "")
                if cur_hint != "":
                    hints.append(escape_string(cur_hint))

        exercise_list.insertExercise(exercise_difficulty, exercise_max_score, exercise_penalty, exercise_type, user.id, str(time.strftime("%Y-%m-%d")), exercise_number, exercise_question, exercise_answer, correct_answer, hints, "en", exercise_title, code)
        return redirect("/l/" + str(listId))

    if exercise_list:
        if exercise_list.created_by != user.id:
            return redirect('/')
        else:
            return render(request, 'createExercise.html', '')
    return redirect('/')


@require_login
def answerQuestion(request, list_id, question_id):
    if request.method == "POST":
        return redirect('/l/' + list_id + '/' + question_id + '/submit')

    exercise_list = object_manager.createExerciseList(list_id)
    if exercise_list:
        all_exercise = exercise_list.allExercises("en")
        current_exercise = None
        for i in all_exercise:
            if i.id == int(question_id):
                current_exercise = i
                break

        if current_exercise:
            return render(request, 'answerQuestion.html', {"exercise": current_exercise,
                                                           "answers": current_exercise.allAnswers(),
                                                           "list_id": list_id,
                                                           "hints": current_exercise.allHints()})
        # If the exercise doesn't exist, redirect to the list page
        else:
            return redirect('/l/' + list_id)
    # Redirect to home if exercise list does't exist
    return redirect('/')

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

@require_login
def submit(request, list_id, question_id):
    user = logged_user(request)
    exercise_list = object_manager.createExerciseList(list_id)
    if exercise_list:
        solved = False
        all_exercise = exercise_list.allExercises("en")
        current_exercise = None
        for i in all_exercise:
            if i.id == int(question_id):
                current_exercise = i
                break

        if current_exercise is None:
            return redirect('/')

        if request.method == 'POST':
            rating = request.POST.get("score")

            # Check which button has been pressed
            if 'b_tryagain' in request.POST:
                # Redirect to the same exercise
                return redirect('/l/' + list_id + '/' + question_id)
            elif 'b_returntolist' in request.POST:
                return redirect('/l/' + list_id)
            elif 'b_nextexercise' in request.POST:
                return redirect('/l/' + list_id + '/' + str(int(question_id) + 1))

            info = object_manager.getInfoForUserForExercise(user.id, question_id)
            penalty = current_exercise.penalty
            current_score = None
            if info is not None:
                current_score = info['exercise_score']

            if current_score is None:
                current_score = current_exercise.max_score

            max_score = current_exercise.max_score
            hint = request.POST.get("used_hints")
            user_output = request.POST.get("code_output")

            if current_exercise.exercise_type == "Open Question":
                selected_answer = request.POST.get("corr_answer")

                if current_exercise.correct_answer == int(selected_answer):
                    # Woohoo right answer!
                    solved = True
                    object_manager.userMadeExercise(question_id, user.id, returnScore(current_score), 1, str(time.strftime("%Y-%m-%d")), 0)

                else:
                    current_score = returnScore(current_score - penalty)

                    object_manager.userMadeExercise(question_id, user.id, current_score, 0, str(time.strftime("%Y-%m-%d")), 0)
                    # return redirect('/l/'+ list_id+ '/'+ question_id)

            elif current_exercise.exercise_type == "Code":
                # For code you only have one answer so lets get it
                correct_answer = stripStr(current_exercise.allAnswers()[0])
                user_output = stripStr(user_output)

                if correct_answer == user_output or (correct_answer == '*' and user_output != ""):
                    current_score = returnScore(current_score - int(hint) * penalty)
                    solved = True
                    object_manager.userMadeExercise(question_id, user.id, current_score, 1, str(time.strftime("%Y-%m-%d")), 0)

                else:
                    # not the right answer! Deduct points!
                    current_score = returnScore(current_score - penalty)
                    object_manager.userMadeExercise(question_id, user.id, current_score, 0, str(time.strftime("%Y-%m-%d")), 0)

            next_exercise = int(question_id) + 1
            if((next_exercise - 1) > len(all_exercise)):
                next_exercise = ""

            return render(request, 'submit.html', {"solved": solved,
                                                   "list_id": list_id,
                                                   "question_id": question_id,
                                                   "current_score": current_score,
                                                   "max_score": max_score,
                                                   "question_type": current_exercise.exercise_type,
                                                   "user_output": user_output,
                                                   "next_exercise": next_exercise})

    else:
        return redirect('/')

def createListElem(elem):
    return """<li class=\"accordion-navigation\">
      <a href=\"#Exerc{id}\">{list_name}</a>
      <div id=\"Exerc{id}\" class=\"content\">
      <div class=\"row\">
      <a href=\"{id}\" class=\"button tiny radius\">Open list</a>
      </div>
      </div>
      </li>""".format(id = elem['id'], list_name = elem['name'])


def listOverview(request):
    # Amount of lists per programming language
    lists_per_prog_lang = statistics_analyzer.AmountOfExerciseListsPerProgrammingLanguage()
    pie_graph = graph_manager.makePieChart('colours', 180
                                           , 100, graphmanager.color_tuples, lists_per_prog_lang['labels'], lists_per_prog_lang['data'])
    # Amount of subjects:
    # colors
    color_info1 = graphmanager.ColorInfo("#F7464A", "#F7464A", "#FF5A5E", "#FF5A5E")
    color_info2 = graphmanager.ColorInfo("#46BFBD", "#46BFBD", "#5AD3D1", "#46BFBD")
    # data
    most_popular_subjects = statistics_analyzer.mostPopularSubjectsTopX(5)
    bar_chart = graph_manager.makeBarChart('subjects', 200, 200,
                                           [color_info2, color_info1], most_popular_subjects['labels'], most_popular_subjects['data'], ["subject"])
    # users with most made lists
    users_with_mosts_made_lists = statistics_analyzer.mostExerciseListsTopX(5)
    bar_chart2 = graph_manager.makeBarChart('activeusers',200,200,[color_info1,color_info2],users_with_mosts_made_lists['labels'],users_with_mosts_made_lists['data'],["#exercises"])


    list_name='%'
    min_list_difficulty=1
    max_list_difficulty=5
    user_first_name='%'
    user_last_name='%'
    prog_lang_name='%'
    subject_name='%'
    order_mode = "ASC"

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
            user_last_name = user_name[1]

        subjects = request.POST.get('subjects')
        if subjects != "":
            subject_name = subjects.split(',')

        order_mode = request.POST.get('order_mode')
        if order_mode == "Ascending":
            order_mode = "ASC"
        else:
            order_mode = "DESC"

        all_lists = object_manager.filterOn(list_name,min_list_difficulty,max_list_difficulty,user_first_name,user_last_name,prog_lang_name,subject_name,order_mode)
        html = ""
        for obj in reversed(all_lists):
            obj['created_on'] = obj['created_on'].strftime("%Y-%m-%d")
            html += createListElem(obj)

        return HttpResponse(html)

    all_lists = object_manager.filterOn(list_name,min_list_difficulty,max_list_difficulty,user_first_name,user_last_name,prog_lang_name,subject_name,order_mode)

    return render(request, 'listOverview.html', {"all_lists": all_lists,
                                                 "languages": object_manager.allProgrammingLanguages(),
                                                 'lists_per_prog_lang_graph': pie_graph,
                                                 'most_popular_subjects': bar_chart,
                                                 'users_with_mosts_made_lists': bar_chart2})
