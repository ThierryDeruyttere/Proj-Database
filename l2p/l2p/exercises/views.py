from django.http import HttpResponse
from django.shortcuts import render, redirect
import sys
from om import *
import dbw
object_manager = objectmanager.ObjectManager()

def test(request):
    languages = dbw.getAll("programmingLanguage")
    return render(request, 'createExerciseList.html',{"languages": languages})