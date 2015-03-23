from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import request

from codegalaxy.evaluation.evaluator import *

def sandbox(request):
    return render(request, 'sandbox.html', {})

def evaluate(request, lang):
    code = request.POST.get('code', '')
    evaluator = EvaluatorCpp(code)
    evaluator.evaluate()
    if evaluator.hasError():
        return HttpResponse(evaluator.getErrorMsg())
    else:
        return HttpResponse(evaluator.output)
