# app/urls.py

from django.urls import path
from .views import QuestionsList, HotQuestions, TagsList, QuestionSingle, Login, Register, AddQuestion, Settings

urlpatterns = [
    path('', QuestionsList, name='QuestionsList'),
    path('hot/', HotQuestions, name='HotQuestions'),
    path('tag/blablabla/', TagsList, name='TagsList'),
    path('question/<int:question_id>', QuestionSingle, name='QuestionSingle'),
    path('login/', Login, name='Login'),
    path('signup/', Register, name='Register'),
    path('ask/', AddQuestion, name='AddQuestion'),
    path('settings/', Settings, name='Settings'),
]