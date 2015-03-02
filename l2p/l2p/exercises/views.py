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
        print(exlist_id)
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
        print(all_exercises)
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
