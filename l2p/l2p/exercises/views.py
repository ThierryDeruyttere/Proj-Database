from django.http import HttpResponse
from django.shortcuts import render, redirect
import sys
from om import *
import dbw
object_manager = objectmanager.ObjectManager()
import time

def test(request):
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
            prog_lang_id = dbw.getIdFromProgLangName(prog_lang)["id"]
            dbw.insertExerciseList(list_name,list_description,int(diff_text),user.id,str(time.strftime("%Y-%m-%d")),prog_lang_id)
            created_list_id = dbw.getMaxIdFromExListForUserID(user.id)
            return redirect("/l/" + str(created_list_id["max"]))


        return render(request, 'createExerciseList.html',{"languages": languages})


def list(request, id=0):
    exercise_list = object_manager.createExerciseList(id)
    if exercise_list:
        prog_lang = dbw.getNameFromProgLangID(exercise_list.programming_language)['name']
        print(prog_lang)

        return render(request, 'list.html', {'id' : id, 'list_name' : exercise_list.name,
                                             'list_description': exercise_list.description,
                                             'list_difficulty': exercise_list.difficulty,
                                             'list_programming_lang': prog_lang})
    else:
        return redirect('/')
