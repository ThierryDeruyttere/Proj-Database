from django.http import HttpResponse
from django.shortcuts import render

import dbw

def home(request):
    # Get choices
    choices = dbw.getAll('polls_choice')

    # Get questions
    questions = dbw.getAll('polls_question')

    # Make list of pairs (question, choice_list)
    l = []
    for question in questions:
        item = {}
        item['question_text'] = question['question_text']
        item['choices'] = [{'choice_text':choice['choice_text']} for choice in choices if choice['question_id'] == question['id']]
        l.append(item)

    return render(request, 'question/index.html', {'test':'haha', 'question_list':l})
