from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.context_processors import request

from codegalaxy.evaluation.evaluators import *

def sandbox(request):
    return render(request, 'sandbox.html', {})

def evaluate(request, lang):
    code = request.POST.get('code', '')

    # Default Evaluator (Python)
    evaluator = EvaluatorPython(code)

    # Other languages
    if lang == 'c++':
        evaluator = EvaluatorCpp(code)
    elif lang == 'sql':
        evaluator = EvaluatorSql(code, 0)

    # Evaluate code
    evaluator.evaluate()

    # Return output
    if evaluator.hasError():
        return HttpResponseBadRequest(evaluator.getErrorMsg())
    else:
        return HttpResponse(evaluator.getOutput())
