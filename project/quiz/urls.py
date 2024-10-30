from django.urls import path

from django.shortcuts import redirect, reverse

from . import views


app_name = 'quiz'
urlpatterns = [
    path('',
         lambda request: redirect(reverse('quiz:quizzes')), name='home'),
    path('dashboard/',
         views.DashboardView.as_view(), name='dashboard'),
    path('settings/',
         views.SettingsView.as_view(), name='settings'),
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
