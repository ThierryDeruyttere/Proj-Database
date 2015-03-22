from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import request


def sandbox(request):
    return render(request, 'sandbox.html', {})

def evaluate(request, lang):
    code = request.POST.get('code', '')
    return HttpResponse("success")
