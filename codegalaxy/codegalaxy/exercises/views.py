from django.shortcuts import render, redirect

import time

from managers.om import *
from codegalaxy.authentication import require_login, logged_user
from managers.om.exercise import Question
from pymysql import escape_string


object_manager = objectmanager.ObjectManager()

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

        while(request.POST.get("subject" + str(current_subject)) != None):
            exercise_list.addSubject(request.POST.get("subject" + str(current_subject)))
            current_subject += 1

        return redirect("/l/" + str(exlist_id))

    return render(request, 'createExerciseList.html', {"languages": languages})


def list(request, id=0):
    exercise_list = object_manager.createExerciseList(id)
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
        if logged_user(request):
            for exercise in all_exercises:
                print(object_manager.getInfoForUserForExercise(logged_user(request).id, exercise.id))
                if object_manager.getInfoForUserForExercise(logged_user(request).id, exercise.id):
                    exercise.solved = True

        correct_user = (logged_user(request).id == exercise_list.created_by)
        return render(request, 'list.html', {'list_name': exercise_list.name,
                                             'list_description': exercise_list.description,
                                             'list_difficulty': exercise_list.difficulty,
                                             'list_programming_lang': prog_lang,
                                             'correct_user': correct_user,
                                             'id': exercise_list.id,
                                             'all_exercises': all_exercises,
                                             'subjects': subjects,
                                             'programming_languages': languages,
                                             'current_prog_lang': current_language})
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

def listOverview(request):
    return render(request, 'listOverview.html', {})
