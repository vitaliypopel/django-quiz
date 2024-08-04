from django.urls import path

from . import views


app_name = 'quiz'
urlpatterns = [
    path('',
         views.HomeView.as_view(), name='home'),
    path('dashboard/',
         views.DashboardView.as_view(), name='dashboard'),
    path('quizzes/',
         views.QuizzesView.as_view(), name='quizzes'),
    path('quizzes/<slug:quiz_title>/',
         views.QuizView.as_view(), name='quiz'),
    path('quizzes/<slug:quiz_title>/<int:question_id>/',
         views.QuizQuestionView.as_view(), name='question'),
    path('quizzes/<slug:quiz_title>/<int:question_id>/<int:choice_id>/',
         views.QuizQuestionChoiceView.as_view(), name='choice'),
    path('quizzes/<slug:quiz_title>/result/',
         views.QuizResultView.as_view(), name='result'),
]
