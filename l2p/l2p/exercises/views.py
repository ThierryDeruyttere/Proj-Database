from django.http import HttpResponse
from django.shortcuts import render, redirect

import sys
import time

import dbw
from om import *
from l2p.authentication import require_login, logged_user
from om.exercise import Question
from pymysql import escape_string

object_manager = objectmanager.ObjectManager()



@require_login
def createExerciseList(request):
    languages = dbw.getAll("programmingLanguage")
    if request.method == 'POST':
        list_name = request.POST.get('list_name', '')
        list_description = request.POST.get('description_text', '')
        difficulty = request.POST.get('difficulty', '')
        prog_lang = request.POST.get('prog_lang', '')
        user = logged_user(request)
        exlist_id = object_manager.insertExerciseList(list_name,list_description,int(difficulty),user.id,str(time.strftime("%Y-%m-%d")),prog_lang)
        return redirect("/l/" + str(exlist_id))

    return render(request, 'createExerciseList.html',{"languages": languages})


def list(request, id=0):
    exercise_list = object_manager.createExerciseList(id)
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name', '')
        dbw.insertSubject(subject_name)
        #get subjectID
        #link with exerciseLIST
        #TODO how to add?

    if exercise_list:
        prog_lang = exercise_list.programming_language_string
        all_exercises = exercise_list.allExercises("en")
        return render(request, 'list.html', {'id' : id, 'list_name' : exercise_list.name,
                                             'list_description': exercise_list.description,
                                             'list_difficulty': exercise_list.difficulty,
                                             'list_programming_lang': prog_lang,
                                             'correct_user': True,
                                             'id': exercise_list.id,
                                             'all_exercises': all_exercises})
    else:
        return redirect('/')

@require_login
def createExercise(request, listId=0):
    exercise_list = object_manager.createExerciseList(listId)
    user = logged_user(request)
    if request.method == 'POST':
        exercise_difficulty = request.POST.get('difficulty')
        exercise_max_score = request.POST.get('max')
        exercise_penalty = request.POST.get('penalty')
        exercise_question_text = escape_string(request.POST.get('Question'))
        exercise_type = request.POST.get('exercise_type')
        hints = []
        for j in range(1,int(exercise_max_score)+1):
            if request.POST.get("hint"+str(j)) != "" and request.POST.get("hint"+str(j)) != None:
                hints.append(escape_string(request.POST.get("hint"+str(j))))

        exercise_number = exercise_list.getLastExercise() + 1

        exercise_question = Question(exercise_question_text,1)
        print(escape_string(exercise_question_text))
        exercise_answer = None
        correct_answer = None
        code = ""
        if(exercise_type == 'Open Question'):
            answer = []
            for i in range(1,6):
                if request.POST.get("answer_no_"+str(i)) != "" and request.POST.get("answer_no_"+str(i)) != None:
                    answer.append(escape_string(request.POST.get("answer_no_"+str(i))))

            selected_answer = request.POST.get("corr_answer")
            exercise_answer = answer
            correct_answer = selected_answer

        else:
            code_for_user = escape_string(request.POST.get("code"))
            expected_answer = escape_string(request.POST.get("output"))
            exercise_answer = [expected_answer]
            correct_answer = 1
            code = code_for_user

        exercise_list.insertExercise(int(exercise_difficulty), int(exercise_max_score), int(exercise_penalty), exercise_type, user.id
                                     ,str(time.strftime("%Y-%m-%d")), exercise_number
                                     ,exercise_question,exercise_answer,correct_answer
                                     ,hints,"en",code)
        return redirect("/l/" + str(listId))

    if exercise_list:
        if exercise_list.created_by != user.id:
            return redirect('/')
        else:
            return render(request, 'createExercise.html','')
    return redirect('/')


@require_login
def answerQuestion(request, list_id, question_id):
    if request.method == "POST":
        return redirect('/l/'+list_id+'/'+question_id+'/submit')

    exercise_list = object_manager.createExerciseList(list_id)
    if exercise_list:
        all_exercise = exercise_list.allExercises("en")
        current_exercise = None
        for i in all_exercise:
            if i.id == int(question_id):
                current_exercise = i
                break


        if current_exercise:
            return render(request, 'answerQuestion.html', {"exercise" : current_exercise,
                                                           "answers": current_exercise.allAnswers(),
                                                           "list_id": list_id,
                                                           "hints": current_exercise.allHints()})

    #Just redirect if list doesn't exist/exericse doens't exist
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

        if request.method == "POST":
            info = object_manager.getInfoForUserForExericse(question_id, user.id)
            penalty= current_exercise.penalty
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
                    #Woohoo right answer!
                    #remove points from using hints
                    solved = True
                    current_score = returnScore(current_score - int(hint)*penalty)
                    object_manager.userMadeExercise(question_id, user.id,  returnScore(current_score), 1, 0)

                else:
                    current_score = returnScore(current_score - penalty)

                    object_manager.userMadeExercise(question_id, user.id,  current_score, 0, 0)
                    #return redirect('/l/'+ list_id+ '/'+ question_id)

            elif current_exercise.exercise_type == "Code":
                #For code you only have one answer so lets get it
                correct_answer = stripStr(current_exercise.allAnswers()[0])
                user_output = stripStr(user_output)
                
                if correct_answer == user_output:
                    solved = True
                    object_manager.userMadeExercise(question_id, user.id,  current_score, 1, 0)
                else:
                    #not the right answer! Deduct points!
                    current_score = returnScore(current_score - penalty)
                    object_manager.userMadeExercise(question_id, user.id,  current_score, 0, 0)

            next_exercise = int(question_id)+1
            if(next_exercise > len(all_exercise)):
                next_exercise = ""

            return render(request, 'submit.html', {"solved" : solved,
                                               "list_id": list_id,
                                               "question_id": question_id,
                                               "current_score": current_score,
                                               "max_score": max_score,
                                               "question_type": current_exercise.exercise_type,
                                               "user_output": user_output,
                                               "next_exercise": next_exercise})

    else:
        return redirect('/')
