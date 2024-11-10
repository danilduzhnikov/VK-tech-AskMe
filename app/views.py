import copy

from django.core.paginator import Paginator
from django.shortcuts import render

from .logic.pagination import paginations_params
QUESTIONS = [
    {
        "title": "title" + str(i),
        "id": str(i),
        "text": "text" + str(i),
    } for i in range(30)
]

HOTQUESTIONS = copy.deepcopy(QUESTIONS)
HOTQUESTIONS.reverse()

# Create your views here.
def Login(request):
    return render(request,
                  'Login.html',
                  context={'questions': QUESTIONS})

def Register(request):
    return render(request,
                  'Register.html',
                  context={'questions': QUESTIONS})

def Settings(request):
    return render(request,
                  'Settings.html',
                  context={'questions': QUESTIONS})

def QuestionsList(request):

    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)

    # вывел монотонную логику отображения пагинатора
    params = paginations_params(page_num, paginator, page)
    return render(request,
                  'QuestionsList.html',
                  context={'questions': page.object_list,
                           'page_obj': page,
                           'paginator': paginator,
                           'params': params}
                  )

def QuestionSingle(request, question_id):
    return render(request,
                  'QuestionSingle.html',
                  context={'question': QUESTIONS[question_id]})

def TagsList(request):
    return render(request,
                  'TagsList.html',
                  context={'questions': QUESTIONS})

def AddQuestion(request):
    return render(request,
                  'AddQuestion.html',
                  context={'questions': QUESTIONS})

def HotQuestions(request):

    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(HOTQUESTIONS, 5)
    page = paginator.page(page_num)

    # вывел монотонную логику отображения пагинатора
    params = paginations_params(page_num, paginator, page)
    return render(request,
                  'HotQuestions.html',
                  context={'questions': page.object_list,
                           'page_obj': page,
                           'paginator': paginator,
                           'params': params}
                  )