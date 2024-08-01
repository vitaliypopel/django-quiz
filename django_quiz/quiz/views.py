from django.shortcuts import render, redirect, reverse
from django.views.generic import View

from .models import Quiz, Question, Choice, UserAnswer


class QuizzesView(View):
    def get(self, request):
        quizzes = Quiz.objects.all()

        return render(
            request,
            template_name='quiz/quizzes.html',
            context={'quizzes': quizzes},
        )


class QuizView(View):
    def get(self, request, quiz_title: str):
        quiz = Quiz.objects.get(url_title=quiz_title)

        return render(
            request,
            template_name='quiz/quiz.html',
            context={'quiz': quiz},
        )


class QuizQuestionView(View):
    def get(self, request, quiz_title: str, question_id: int):
        quiz = Quiz.objects.get(url_title=quiz_title)
        question = Question.objects.filter(quiz=quiz)[question_id - 1]
        choices = Choice.objects.filter(question=question)

        return render(
            request,
            template_name='quiz/question.html',
            context={
                'quiz': quiz,
                'question': question,
                'choices': choices,
                'question_id': question_id,
            },
        )

    def post(self, request, quiz_title: str, question_id: int):
        choice = Choice.objects.get(
            pk=int(request.POST.get('choice'))
        )
        session = request.session.session_key

        UserAnswer.objects.create(
            choice=choice,
            session=session,
        )

        return redirect(reverse(
            viewname='quiz:question',
            args=(quiz_title, question_id + 1)
        ))


class QuizResultView(View):
    def get(self, request, quiz_title: str):
        ...
