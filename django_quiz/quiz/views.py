from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from django.views.generic import View, ListView, DetailView, RedirectView

from .models import Quiz, Question, Choice, Answer, CompletedQuiz
from .utils import get_user_session


class HomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('quiz:quizzes')


class QuizzesView(ListView):
    template_name = 'quiz/quizzes.html'
    model = Quiz
    context_object_name = 'quizzes'


class QuizView(DetailView):
    template_name = 'quiz/quiz.html'
    model = Quiz
    context_object_name = 'quiz'

    def get_object(self):
        return get_object_or_404(self.model, url_title=self.kwargs['quiz_title'])


class QuizQuestionView(View):
    def get(self, request, quiz_title: str, question_id: int):
        ...


class QuizQuestionChoiceView(View):
    def post(self, request, quiz_title: str, question_id: int, choice_id: int):
        ...


class QuizResultView(View):
    def get(self, request, quiz_title: str):
        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        answers = Answer.objects.filter(
            user_session=get_user_session(request),
            quiz=quiz,
        )
        rating = answers.filter(is_correct=True).count()

        return render(
            request,
            template_name='quiz/result.html',
            context={
                'quiz': quiz,
                'answers': answers,
                'rating': rating,
            },
        )


class DashboardView(View):
    def get(self, request):
        user_session = get_user_session(request)
        return render(
            request,
            template_name='quiz/dashboard.html',
            context={'user_session': user_session},
        )
