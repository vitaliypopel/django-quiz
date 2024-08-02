from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import View, ListView, DetailView

from .models import Quiz, Question, Choice, UserAnswer
from .utils import get_session


class QuizzesView(ListView):
    template_name = 'quiz/quizzes.html'
    model = Quiz
    context_object_name = 'quizzes'


class QuizView(DetailView):
    template_name = 'quiz/quiz.html'
    model = Quiz
    context_object_name = 'quiz'

    def get_object(self):
        url_title = self.kwargs['quiz_title']
        return get_object_or_404(self.model, url_title=url_title)


class QuizQuestionView(View):
    def get(self, request, quiz_title: str, question_id: int):
        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        question = get_object_or_404(Question, quiz=quiz, number=question_id)

        return render(
            request,
            template_name='quiz/question.html',
            context={
                'quiz': quiz,
                'question': question,
            },
        )

    def post(self, request, quiz_title: str, question_id: int):
        choice_id = int(request.POST.get('choice'))
        session = get_session(request)
        next_question_id = question_id + 1

        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        question = get_object_or_404(Question, quiz=quiz, number=question_id)
        choice = get_object_or_404(Choice, question=question, pk=choice_id)

        UserAnswer.objects.create(
            quiz=quiz,
            question=question,
            choice=choice,
            is_correct=choice.is_correct,
            session=session,
        )

        questions = Question.objects.filter(quiz=quiz, number=next_question_id)
        if not questions:
            return redirect(reverse(
                viewname='quiz:result',
                args=(quiz_title,),
            ))

        return redirect(reverse(
            viewname='quiz:question',
            args=(quiz.url_title, next_question_id),
        ))


class QuizResultView(View):
    def get(self, request, quiz_title: str):
        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        user_answers = UserAnswer.objects.filter(
            quiz=quiz,
            session=get_session(request),
        )
        rating = user_answers.filter(is_correct=True).count()

        return render(
            request,
            template_name='quiz/result.html',
            context={
                'quiz': quiz,
                'user_answers': user_answers,
                'rating': rating,
            },
        )


class Dashboard(View):
    def get(self, request):
        session = get_session(request)
        return render(
            request,
            template_name='quiz/dashboard.html',
            context={'session': session},
        )
