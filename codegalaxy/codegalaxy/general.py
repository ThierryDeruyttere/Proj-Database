from django.core.context_processors import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from managers.om import *
object_manager = objectmanager.ObjectManager()

def getBrowserLanguage(request):
    if request.LANGUAGE_CODE.startswith("en"):
        return object_manager.getLanguageObject("en")
    return object_manager.getLanguageObject(request.LANGUAGE_CODE)

# Strips string from \n or \r
def stripStr(string, extra=False):
    strip = ["\n", "\r"]
    s = string
    for i in strip:
        if extra:
            s = s.replace(i, " ")
        else:
            s = s.replace(i, "")
    return s
