from tkinter.font import names

from django.urls import path

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView

from . import views


app_name = 'quiz'
urlpatterns = [
    path('',
         lambda request: redirect(reverse('quiz:quizzes')), name='home'),
    path('quizzes/create/',
         views.CreateQuizView.as_view(), name='create_quiz'),
    path('quizzes/<slug:quiz_title>/manage/',
         views.ManageQuizView.as_view(), name='manage_quiz'),
    path('dashboard/',
         views.DashboardView.as_view(), name='dashboard'),
    path('profile/<slug:username>/',
         views.ProfileView.as_view(), name='profile'),
    path('settings/',
         views.GeneralSettingsView.as_view(), name='settings'),
    path('settings/account/',
         views.AccountSettingsView.as_view(), name='account_settings'),
    path('settings/security/',
         views.SecuritySettingsView.as_view(), name='security_settings'),
    path('quizzes/',
         views.QuizzesView.as_view(), name='quizzes'),
    path('quizzes/<slug:quiz_title>/',
         views.QuizView.as_view(), name='quiz'),
    path('quizzes/<slug:quiz_title>/<int:question_id>/',
         views.QuizQuestionView.as_view(), name='question'),
    path('quizzes/<slug:quiz_title>/<int:question_id>/answer/',
         views.QuizAnswerView.as_view(), name='answer'),
    path('quizzes/<slug:quiz_title>/<int:question_id>/complete/',
         views.QuizCompleteView.as_view(), name='complete'),
    path('quizzes/<slug:quiz_title>/result/',
         views.QuizResultView.as_view(), name='result'),
    path('quizzes/<slug:quiz_title>/again/',
         views.QuizTakeAgainView.as_view(), name='again'),
]
