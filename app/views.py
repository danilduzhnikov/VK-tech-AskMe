import copy

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.forms import LoginForm, RegisterForm
from app.utils import paginations_params, questions_list_tags

from app.models import Tag, Question, QuestionTag

QUESTIONS = Question.objects.get_new_questions()

POPULAR_TAGS = Tag.objects.get_popular()

HOTQUESTIONS = Question.objects.get_hot_questions()



# Create your views here.
def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, login=login, password=password)
            if user:
                auth.login(request, user)
                return redirect('QuestionsList')
    else:
        form = LoginForm()
    return render(request,
                  'Login.html',
                  context={'questions': QUESTIONS,
                           'form': form})

def Logout(request):
    auth.logout(request)
    return redirect('Login')

def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            auth.login(request, user)
            return redirect('QuestionsList')
    else:
        form = RegisterForm()
    return render(request,
                  'Register.html',
                  context={'questions': QUESTIONS,
                           'form': form})
@login_required
def Settings(request):
    return render(request,
                  'Settings.html',
                  context={'questions': QUESTIONS})

def QuestionsList(request):
    data = QUESTIONS
    pagination = paginations_params(request, data, 5)
    page_objects = pagination.get("page_objects")
    questions = questions_list_tags(page_objects)
    return render(request,
                  'QuestionsList.html',
                  context={'pagination_params': pagination.get("params"),
                           'questions': questions}
                  )
def HotQuestions(request):
    data = HOTQUESTIONS
    pagination = paginations_params(request, data, 5)
    page_objects = pagination.get("page_objects")
    questions = questions_list_tags(page_objects)
    return render(request,
                  'HotQuestions.html',
                  context={'pagination_params': pagination.get("params"),
                           'questions': questions}
                  )
def QuestionSingle(request, question_id):
    question = Question.objects.get(id=question_id)
    questions_tags = questions_list_tags(question)
    return render(request,
                  'QuestionSingle.html',
                  context={'question': question,
                           'questions_tags': questions_tags})

def TagsList(request, tag):
    data = QuestionTag.objects.get_questions_per_tag(tag)
    pagination = paginations_params(request, data, 5)
    page_objects = pagination.get("page_objects")
    questions = questions_list_tags(page_objects)
    return render(request,
                  'TagsList.html',
                  context={'tag': tag,
                           'pagination_params': pagination.get("params"),
                           'questions': questions})

def AddQuestion(request):
    return render(request,
                  'AddQuestion.html',
                  context={'questions': QUESTIONS})
