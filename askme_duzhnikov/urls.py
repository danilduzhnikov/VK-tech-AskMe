"""
URL configuration for askme_duzhnikov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.QuestionsList, name='QuestionsList'),
    path('hot/', views.HotQuestions, name='HotQuestions'),
    path('tag/blablabla/', views.TagsList, name='TagsList'),
    path('question/<int:question_id>', views.QuestionSingle, name='QuestionSingle'),
    path('login/', views.Login, name='Login'),
    path('signup/', views.Register, name='Register'),
    path('ask/', views.AddQuestion, name='AddQuestion'),
    path('settings/', views.Settings, name='Settings'),

]
