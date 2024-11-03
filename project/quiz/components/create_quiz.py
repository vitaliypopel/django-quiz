from django_unicorn.components import UnicornView

from django.shortcuts import redirect, reverse

from quiz.models import Quiz


class CreateQuizView(UnicornView):
    quizzes = Quiz.objects.all()

    title = ''
    descriptions = ''
    complexity = None

    def url_title(self):
        return self.title.lower().replace(' ', '-')

    def is_title_taken(self):
        if self.url_title() == 'create':
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

    def get_data(self):
        return {
            'title': self.title,
            'url_title': self.url_title(),
            'descriptions': self.descriptions,
            'complexity': self.complexity,
            'author': self.request.user,
        }

    def create_quiz(self):
        Quiz.objects.create(**self.get_data())
        return redirect(reverse(
            viewname='quiz:quiz',
            args=(self.url_title(),),
        ))
