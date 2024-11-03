from django_unicorn.components import UnicornView

from django.shortcuts import redirect, reverse

from quiz.models import Quiz, Question


class EditQuizView(UnicornView):
    quizzes = Quiz.objects.all()

    title = ''
    descriptions = ''
    complexity = None

    quiz: Quiz
    questions: list[Question]

    def mount(self):
        url_title = self.request.path.replace('/quizzes/', '').replace('/edit/', '')

        self.quiz = Quiz.objects.get(url_title=url_title)
        self.questions = Question.objects.filter(quiz=self.quiz)

        self.title = self.quiz.title
        self.descriptions = self.quiz.descriptions
        self.complexity = self.quiz.complexity

    def url_title(self):
        return self.title.lower().replace(' ', '-')

    def is_title_taken(self):
        if self.url_title() == 'create':
            return True
        elif self.url_title() == self.quiz.url_title:
            return False
        return self.quizzes.filter(url_title=self.url_title()).exists()

    def is_title_length_valid(self):
        return True if self.title == '' else 2 <= len(self.title) <= 100

    def is_descriptions_length_valid(self):
        return True if self.descriptions == '' else 10 <= len(self.descriptions) <= 2000

    def is_form_valid(self):
        if not self.is_title_taken() and \
            self.is_title_length_valid() and \
            self.is_descriptions_length_valid() and \
            self.complexity is not None:
            return True
        return False

    def edit_quiz(self):
        self.quiz.url_title = self.url_title()
        self.quiz.title = self.title
        self.quiz.descriptions = self.descriptions
        self.quiz.complexity = self.complexity

        self.quiz.save()
        return redirect(reverse(
            viewname='quiz:quiz',
            args=(self.quiz.url_title,),
        ))
