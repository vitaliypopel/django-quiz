from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.generic import DetailView, FormView, ListView, TemplateView, View

from .models import Quiz, Question, Choice, Answer, CompletedQuiz
from .forms import UserForm


@method_decorator(require_GET, name='dispatch')
class QuizzesView(ListView):
    template_name = 'quiz/quizzes.html'
    model = Quiz
    context_object_name = 'quizzes'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by')
        if not sort_by:
            return queryset
        return queryset.order_by(sort_by)


@method_decorator(require_GET, name='dispatch')
class QuizView(DetailView):
    template_name = 'quiz/quiz.html'
    model = Quiz
    context_object_name = 'quiz'

    def get_object(self):
        return get_object_or_404(self.model, url_title=self.kwargs['quiz_title'])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        if self.request.user.is_authenticated:
            completed_quiz = CompletedQuiz.objects.filter(
                quiz=self.get_object(),
                user=self.request.user,
            )
            if completed_quiz.exists():
                context_data['is_completed'] = completed_quiz.first().is_completed
        return context_data



@method_decorator(decorator=[require_GET, login_required], name='dispatch')
class QuizQuestionView(View):
    def get(self, request, quiz_title: str, question_id: int):
        user = request.user

        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        question = get_object_or_404(Question, quiz=quiz, number=question_id)

        completed_quiz = CompletedQuiz.objects.filter(
            user=user,
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
                user=user,
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
                    user=user,
                    quiz=quiz,
                    question=previous_question,
                )

                if not answer.exists():
                    return redirect(reverse(
                        viewname='quiz:question',
                        args=(quiz_title, previous_question_id),
                    ))

        answer = Answer.objects.filter(
            user=user,
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


@method_decorator(decorator=[require_POST, login_required], name='dispatch')
class QuizAnswerView(View):
    def post(self, request, quiz_title: str, question_id: int):
        user = request.user

        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        question = get_object_or_404(Question, quiz=quiz, number=question_id)

        choice_id = int(request.POST.get('choice'))
        choice = get_object_or_404(Choice, pk=choice_id)

        Answer.objects.create(
            user=user,
            quiz=quiz,
            question=question,
            choice=choice,
            is_correct=choice.is_correct,
        )

        return redirect(reverse(
            viewname='quiz:question',
            args=(quiz_title, question_id + 1),
        ))


@method_decorator(decorator=[require_POST, login_required], name='dispatch')
class QuizCompleteView(View):
    def post(self, request, quiz_title: str, question_id: int):
        user = request.user

        quiz = get_object_or_404(Quiz, url_title=quiz_title)
        question = get_object_or_404(Question, quiz=quiz, number=question_id)

        choice_id = int(request.POST.get('choice'))
        choice = get_object_or_404(Choice, pk=choice_id)

        with transaction.atomic():
            Answer.objects.create(
                user=user,
                quiz=quiz,
                question=question,
                choice=choice,
                is_correct=choice.is_correct,
            )

            completed_quiz = get_object_or_404(
                CompletedQuiz,
                user=user,
                quiz=quiz
            )

            completed_quiz.result = Answer.objects.filter(
                user=user,
                quiz=quiz,
                is_correct=True,
            ).count()
            completed_quiz.is_completed = True

            completed_quiz.save()

        return redirect(reverse(
            viewname='quiz:result',
            args=(quiz_title,),
        ))


@method_decorator(decorator=[require_POST, login_required], name='dispatch')
class QuizTakeAgainView(View):
    def post(self, request, quiz_title: str):
        user = request.user
        quiz = get_object_or_404(Quiz, url_title=quiz_title)

        answers = Answer.objects.filter(
            user=user,
            quiz=quiz,
        )
        completed_quiz = CompletedQuiz.objects.get(
            user=user,
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


@method_decorator(decorator=[require_GET, login_required], name='dispatch')
class QuizResultView(View):
    def get(self, request, quiz_title: str):
        user = request.user
        quiz = get_object_or_404(Quiz, url_title=quiz_title)

        completed_quiz = CompletedQuiz.objects.filter(
            user=user,
            quiz=quiz,
            is_completed=True,
        )
        if not completed_quiz.exists():
            return redirect(reverse(
                viewname='quiz:question',
                args=(quiz_title, 1),
            ))

        answers = Answer.objects.filter(
            user=user,
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


@method_decorator(decorator=[require_GET, login_required], name='dispatch')
class DashboardView(View):
    def get(self, request):
        completed_quizzes = CompletedQuiz.objects.filter(
            user=request.user,
        )
        return render(
            request,
            template_name='quiz/dashboard.html',
            context={
                'completed_quizzes': completed_quizzes.filter(is_completed=True),
                'not_completed_quizzes': completed_quizzes.filter(is_completed=False),
            },
        )


@method_decorator(decorator=[require_http_methods(['GET', 'POST']), login_required], name='dispatch')
class CreateQuizView(View):
    def get(self, request):
        return render(request, template_name='quiz/create_quiz.html')

    def post(self, request):
        new_quiz_data = {
            'title': request.POST.get('quiz_title'),
            'url_title': request.POST.get('quiz_url_title'),
            'descriptions': request.POST.get('quiz_descriptions'),
            'complexity': request.POST.get('quiz_complexity'),
        }
        new_quiz = Quiz.objects.create(**new_quiz_data)
        return redirect(reverse(
            viewname='quiz:quiz',
            args=(new_quiz.url_title,),
        ))


@method_decorator(decorator=[require_http_methods(['GET', 'POST']), login_required], name='dispatch')
class GeneralSettingsView(View):
    COLORS = {
        'green': 'success',
        'blue': 'primary',
        'red': 'danger',
        'yellow': 'warning',
        'cyan': 'info',
        'gray': 'secondary',
    }

    def get(self, request):
        return render(
            request,
            template_name='quiz/settings.html',
            context={'colors': self.COLORS},
        )

    def post(self, request):
        response = redirect(reverse('quiz:settings'))

        theme = request.POST.get('theme')
        if theme is not None:
            response.set_cookie('theme', theme)

        color_theme = request.POST.get('color_theme')
        if color_theme is not None:
            response.set_cookie('color_theme', color_theme)

        return response


@method_decorator(decorator=[require_http_methods(['GET', 'POST']), login_required], name='dispatch')
class AccountSettingsView(FormView):
    form_class = UserForm
    template_name = 'quiz/account_settings.html'
    success_url = reverse_lazy('quiz:account_settings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(decorator=[require_GET, login_required], name='dispatch')
class SecuritySettingsView(TemplateView):
    template_name = 'quiz/security_settings.html'
