from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.context_processors import request

from codegalaxy.evaluation.evaluators import *

# The view for sandbox.html
def sandbox(request):
    return render(request, 'sandbox.html', {})

def evaluate(request, lang):
    # Get data from POST request
    code = request.POST.get('code', '')
    is_editor = request.POST.get('is_editor', '') != ''

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
        return HttpResponseBadRequest(evaluator.getErrorMsg(is_editor))
    else:
        return HttpResponse(evaluator.getOutput(is_editor))
