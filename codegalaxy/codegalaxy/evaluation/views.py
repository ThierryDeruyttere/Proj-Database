from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import request

from codegalaxy.evaluation.evaluator import *

def sandbox(request):
    return render(request, 'sandbox.html', {})

def evaluate(request, lang):
    code = request.POST.get('code', '')
    response = EvaluatorCpp(code).evaluate()
    if response.error:
        return HttpResponse(response.error)
    else:
        return HttpResponse(response.output)
