from django.http import HttpResponse
from django.shortcuts import render, redirect
import sys
from om import *
import dbw
object_manager = objectmanager.ObjectManager()
import time


def createExerciseList(request):
    if 'current_user' not in request.session:
        return redirect("/login")
    else:
        languages = dbw.getAll("programmingLanguage")
        if request.method == 'POST':
            list_name = request.POST.get('list_name', '')
            list_description = request.POST.get('description_text', '')
            difficulty = request.POST.get('difficulty', '')
            prog_lang = request.POST.get('prog_lang', '')
            user = object_manager.createUser(id = request.session['current_user'])
            prog_lang_id = dbw.getIdFromProgrammingLanguage(prog_lang)["id"]
            exlist_id = object_manager.insertExerciseList(list_name,list_description,int(difficulty),user.id,str(time.strftime("%Y-%m-%d")),prog_lang_id)
            return redirect("/l/" + str(exlist_id))


        return render(request, 'createExerciseList.html',{"languages": languages})


def list(request, id=0):
    exercise_list = object_manager.createExerciseList(id)
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name', '')
        dbw.insertSubject(subject_name)
        #get subjectID
        #link with exerciseLIST
        #TODO

    if exercise_list:
        prog_lang = dbw.getNameFromProgLangID(exercise_list.programming_language)['name']

        return render(request, 'list.html', {'id' : id, 'list_name' : exercise_list.name,
                                             'list_description': exercise_list.description,
                                             'list_difficulty': exercise_list.difficulty,
                                             'list_programming_lang': prog_lang,
                                             'correct_user': True,
                                             'id': exercise_list.id})
    else:
        return redirect('/')


def createExercise(request, listId=0):
    if 'current_user' not in request.session:
        return redirect("/login")

    if request.method == 'POST':
        exercise_difficulty = request.POST.get('difficulty')
        exercise_max_score = request.POST.get('max')
        exercise_penalty = request.POST.get('penalty')
        exercise_question = request.POST.get('Question')
        exercise_type = request.POST.get('exercise_type')
        if(exercise_type == 'Open Question'):
            print("open")
        else:
            print("code")


    exercise_list = object_manager.createExerciseList(listId)
    if exercise_list:
        user = object_manager.createUser(id = request.session['current_user'])
        if exercise_list.created_by != user.id:
            return redirect('/')
        else:
            return render(request, 'createExercise.html','')
    return redirect('/')
