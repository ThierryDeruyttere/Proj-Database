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
            diff_text = request.POST.get('diff_text', '')
            prog_lang = request.POST.get('prog_lang', '')
            user = object_manager.createUser(id = request.session['current_user'])
            prog_lang_id = dbw.getIdFromProgrammingLanguage(prog_lang)["id"]
            exlist_id = object_manager.InsertExerciseList(list_name,list_description,int(diff_text),user.id,str(time.strftime("%Y-%m-%d")),prog_lang_id)
            return redirect("/l/" + str(exlist_id))


        return render(request, 'createExerciseList.html',{"languages": languages})


def list(request, id=0):
    exercise_list = object_manager.createExerciseList(id)
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

    exercise_list = object_manager.createExerciseList(listId)
    if exercise_list:
        user = object_manager.createUser(id = request.session['current_user'])
        if exercise_list.created_by != user.id:
            return redirect('/')
        else:

            return render(request, 'createExercise.html','')
    return redirect('/')