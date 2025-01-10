import copy

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.forms import LoginForm, RegisterForm, AddQuestionForm, AddAnswerForm
from app.utils import paginations_params, get_tags_per_question

from app.models import Tag, Question, QuestionTag, QuestionLike

QUESTIONS = Question.objects.get_new_questions()

POPULAR_TAGS = Tag.objects.get_popular()

HOTQUESTIONS = Question.objects.get_hot_questions()



# Create your views here.
def Login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = auth.authenticate(request,
                                 login=form.cleaned_data['login'],
                                 password=form.cleaned_data['password'])
        if user:
            auth.login(request, user)
            return redirect('QuestionsList')
    return render(request,
                  'Login.html',
                  context={'questions': QUESTIONS,
                           'form': form})

def Logout(request):
    auth.logout(request)
    return redirect('Login')

def Register(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=True)
        auth.login(request, user)
        return redirect('QuestionsList')

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
    questions = get_tags_per_question(page_objects, request.user)
    return render(request,
                  'QuestionsList.html',
                  context={'pagination_params': pagination.get("params"),
                           'questions': questions}
                  )
def HotQuestions(request):
    data = HOTQUESTIONS
    pagination = paginations_params(request, data, 5)
    page_objects = pagination.get("page_objects")
    questions = get_tags_per_question(page_objects)
    return render(request,
                  'HotQuestions.html',
                  context={'pagination_params': pagination.get("params"),
                           'questions': questions}
                  )
def QuestionSingle(request, question_id):
    question_single = Question.objects.get(id=question_id)
    answers = question_single.answer_set.all()

    pagination = paginations_params(request, answers, 2)
    page_objects = pagination.get("page_objects")
    questions = get_tags_per_question(question_single)

    if request.user.is_authenticated:
        form = AddAnswerForm(request.POST or None)
        if form.is_valid():
            form.save(author=request.user, question=question_single)
            return redirect('QuestionSingle', question_id=question_id)
    else:
        return redirect('Login')

    return render(request,
                  'QuestionSingle.html',
                  context={'pagination_params': pagination.get("params"),
                           'answers': page_objects,
                           'questions': questions,  # Single question in list
                           'form': form})

def TagsList(request, tag):
    data = QuestionTag.objects.get_questions_per_tag(tag)
    pagination = paginations_params(request, data, 5)
    page_objects = pagination.get("page_objects")
    questions = get_tags_per_question(page_objects)
    return render(request,
                  'TagsList.html',
                  context={'tag': tag,
                           'pagination_params': pagination.get("params"),
                           'questions': questions})
@login_required
def AddQuestion(request):
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=True, author=request.user)
            return redirect('QuestionSingle', question_id=question.id)
    else:
        form = AddQuestionForm()

    return render(request, 'AddQuestion.html', context={'form': form})
@login_required
def LikeAsync(request, question_id):
        likesCount = QuestionLike.objects.get_count_likes_question(question_id)
        if QuestionLike.objects.is_user_liked_question(request.user, question_id):
            QuestionLike.objects.filter(user=request.user, question_id=question_id).delete()
            return JsonResponse({'likes_count': f"{likesCount - 1}",
                                 'is_liked': 'false'})
        else:
            QuestionLike.objects.create(user=request.user, question_id=question_id)
            return JsonResponse({'likes_count': f"{likesCount + 1}",
                                 'is_liked': 'true'})
