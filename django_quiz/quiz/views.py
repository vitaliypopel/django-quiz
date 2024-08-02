from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
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
        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        return render(
            request,
            template_name='quiz/quiz.html',
            context={'quiz': quiz},
        )


class QuizQuestionView(View):
    def get(self, request, quiz_title: str, question_id: int):
        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        questions = Question.objects.filter(quiz=quiz, number=question_id)
        if not questions:
            return redirect(reverse(
                viewname='quiz:result',
                args=(quiz_title,),
            ))

        return render(
            request,
            template_name='quiz/question.html',
            context={
                'quiz': quiz,
                'question': questions.first(),
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
            args=(quiz_title, question_id + 1),
        ))


class QuizResultView(View):
    def get(self, request, quiz_title: str):
        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        return render(
            request,
            template_name='quiz/result.html',
            context={'quiz': quiz},
        )
