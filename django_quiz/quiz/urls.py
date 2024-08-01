from django.urls import path

from . import views


app_name = 'quiz'
urlpatterns = [
    path(
        '',
        views.QuizzesView.as_view(),
        name='quizzes'
    ),
    path(
        '<slug:quiz_title>/',
        views.QuizView.as_view(),
        name='quiz'
    ),
    path(
        '<slug:quiz_title>/<int:question_id>/',
        views.QuizQuestionView.as_view(),
        name='question'
    ),
]
