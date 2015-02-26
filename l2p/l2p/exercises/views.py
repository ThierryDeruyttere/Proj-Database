from django.http import HttpResponse
from django.shortcuts import render, redirect
import sys
from om import *
import dbw
object_manager = objectmanager.ObjectManager()

def test(request):
    if request.method == 'POST':
        list_name = request.POST.get('list_name', '')
        list_description = request.POST.get('description_text', '')
        diff_text = request.POST.get('diff_text', '')
        prog_lang = request.POST.get('prog_lang', '')
        print(list_name)
        print(list_description)
        print(diff_text)
        print(prog_lang)

    languages = dbw.getAll("programmingLanguage")
    return render(request, 'createExerciseList.html',{"languages": languages})