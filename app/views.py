import copy

from django.shortcuts import render
from app.utils import paginations_params, questions_list_tags

from app.models import Tag, Question

QUESTIONS = Question.objects.get_new_questions()

POPULAR_TAGS = Tag.objects.get_popular()

HOTQUESTIONS = Question.objects.get_hot_questions()

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
    pagination = paginations_params(request, QUESTIONS, 5)
    questions = pagination.get("page_objects")
    questions_tags = questions_list_tags(questions)
    return render(request,
                  'QuestionsList.html',
                  context={'pagination_params': pagination.get("params"),
                           'questions_tags': questions_tags}
                  )

def QuestionSingle(request, question_id):
    question = Question.objects.get(id=question_id)
    questions_tags = questions_list_tags(question)
    return render(request,
                  'QuestionSingle.html',
                  context={'question': question,
                           'questions_tags': questions_tags})

def TagsList(request):
    return render(request,
                  'TagsList.html',
                  context={'questions': QUESTIONS})

def AddQuestion(request):
    return render(request,
                  'AddQuestion.html',
                  context={'questions': QUESTIONS})

def HotQuestions(request):
    pagination = paginations_params(request, HOTQUESTIONS, 6)
    return render(request,
                  'HotQuestions.html',
                  context={'questions': pagination.get("page_objects"),     # Input data for question layout
                           'pagination_params': pagination.get("params")}   # Parameters for pagination layout
                  )