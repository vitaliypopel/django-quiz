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
        session = request.session.session_key
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
        user_answers = get_list_or_404(
            UserAnswer,
            quiz=quiz,
            session=request.session.session_key
        )

        return render(
            request,
            template_name='quiz/result.html',
            context={
                'quiz': quiz,
                'user_answers': user_answers,
            },
        )
