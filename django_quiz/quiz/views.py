from django.db import transaction
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import View, ListView, DetailView, RedirectView

from .models import Quiz, Question, Choice, Answer, CompletedQuiz
from .utils import get_user_session


@method_decorator(require_GET, name='dispatch')
class HomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('quiz:quizzes')


@method_decorator(require_GET, name='dispatch')
class QuizzesView(ListView):
    template_name = 'quiz/quizzes.html'
    model = Quiz
    context_object_name = 'quizzes'


@method_decorator(require_GET, name='dispatch')
class QuizView(DetailView):
    template_name = 'quiz/quiz.html'
    model = Quiz
    context_object_name = 'quiz'

    def get_object(self):
        return get_object_or_404(self.model, url_title=self.kwargs['quiz_title'])


@method_decorator(require_GET, name='dispatch')
class QuizQuestionView(View):
    def get(self, request, quiz_title: str, question_id: int):
        user_session = get_user_session(request)

        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        question = get_object_or_404(Question, quiz=quiz, number=question_id)

        completed_quiz = CompletedQuiz.objects.filter(
            user_session=user_session,
            quiz=quiz,
        )
        if completed_quiz.exists():
            if completed_quiz.first().is_completed:
                return redirect(reverse(
                    viewname='quiz:result',
                    args=(quiz_title,),
                ))
        else:
            CompletedQuiz.objects.create(
                user_session=user_session,
                quiz=quiz,
                is_completed=False,
            )

        if question_id > 1:
            previous_questions = Question.objects.filter(
                quiz=quiz,
            )[:question_id - 1][::-1]

            for (
                    previous_question_id,
                    previous_question
            ) in enumerate(previous_questions, start=question_id - 1):
                answer = Answer.objects.filter(
                    user_session=user_session,
                    quiz=quiz,
                    question=previous_question,
                )

                if not answer.exists():
                    return redirect(reverse(
                        viewname='quiz:question',
                        args=(quiz_title, previous_question_id),
                    ))

        answer = Answer.objects.filter(
            user_session=user_session,
            quiz=quiz,
            question=question,
        )
        if answer.exists() and not question.is_last:
            return redirect(reverse(
                viewname='quiz:question',
                args=(quiz_title, question_id + 1),
            ))

        return render(
            request,
            template_name='quiz/question.html',
            context={
                'quiz': quiz,
                'question': question,
            },
        )


@method_decorator(require_POST, name='dispatch')
class QuizAnswerView(View):
    def post(self, request, quiz_title: str, question_id: int):
        user_session = get_user_session(request)

        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        question = get_object_or_404(Question, quiz=quiz, number=question_id)

        choice_id = int(request.POST.get('choice'))
        choice = get_object_or_404(Choice, pk=choice_id)

        Answer.objects.create(
            user_session=user_session,
            quiz=quiz,
            question=question,
            choice=choice,
            is_correct=choice.is_correct,
        )

        return redirect(reverse(
            viewname='quiz:question',
            args=(quiz_title, question_id + 1),
        ))


@method_decorator(require_POST, name='dispatch')
class QuizCompleteView(View):
    def post(self, request, quiz_title: str, question_id: int):
        user_session = get_user_session(request)

        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        question = get_object_or_404(Question, quiz=quiz, number=question_id)

        choice_id = int(request.POST.get('choice'))
        choice = get_object_or_404(Choice, pk=choice_id)

        Answer.objects.create(
            user_session=user_session,
            quiz=quiz,
            question=question,
            choice=choice,
            is_correct=choice.is_correct,
        )

        completed_quiz = get_object_or_404(
            CompletedQuiz,
            user_session=user_session,
            quiz=quiz
        )

        completed_quiz.result = Answer.objects.filter(
            user_session=user_session,
            quiz=quiz,
            is_correct=True,
        ).count()
        completed_quiz.is_completed = True

        completed_quiz.save()

        return redirect(reverse(
            viewname='quiz:result',
            args=(quiz_title,),
        ))


@method_decorator(require_POST, name='dispatch')
class QuizTakeAgainView(View):
    def post(self, request, quiz_title: str):
        user_session = get_user_session(request)
        quiz = get_object_or_404(Quiz, url_title=quiz_title)

        answers = Answer.objects.filter(
            user_session=user_session,
            quiz=quiz,
        )
        completed_quiz = CompletedQuiz.objects.get(
            user_session=user_session,
            quiz=quiz,
        )

        with transaction.atomic():
            answers.delete()
            completed_quiz.result = 0
            completed_quiz.is_completed = False
            completed_quiz.save()

        return redirect(reverse(
            viewname='quiz:question',
            args=(quiz_title, 1),
        ))


@method_decorator(require_GET, name='dispatch')
class QuizResultView(View):
    def get(self, request, quiz_title: str):
        user_session = get_user_session(request)
        quiz = get_object_or_404(Quiz, url_title=quiz_title)

        completed_quiz = CompletedQuiz.objects.filter(
            user_session=user_session,
            quiz=quiz,
            is_completed=True,
        )
        if not completed_quiz.exists():
            return redirect(reverse(
                viewname='quiz:question',
                args=(quiz_title, 1),
            ))

        answers = Answer.objects.filter(
            user_session=get_user_session(request),
            quiz=quiz,
        )

        return render(
            request,
            template_name='quiz/result.html',
            context={
                'completed_quiz': completed_quiz.first(),
                'answers': answers,
            },
        )


@method_decorator(require_GET, name='dispatch')
class DashboardView(View):
    def get(self, request):
        user_session = get_user_session(request)
        completed_quizzes = CompletedQuiz.objects.filter(
            user_session=user_session,
            is_completed=True,
        )
        return render(
            request,
            template_name='quiz/dashboard.html',
            context={
                'user_session': user_session,
                'completed_quizzes': completed_quizzes,
            },
        )
