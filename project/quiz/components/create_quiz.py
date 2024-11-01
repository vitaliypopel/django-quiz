from django_unicorn.components import UnicornView

from quiz.models import Quiz


class CreateQuizView(UnicornView):
    quiz_title = ''
    quiz_descriptions = ''
    quiz_complexity = None

    def quiz_url_title(self):
        return self.quiz_title.lower().replace(' ', '-')

    def is_quiz_title_taken(self):
        return Quiz.objects.filter(url_title=self.quiz_url_title()).exists()

    def is_quiz_title_length_valid(self):
        return True if self.quiz_title == '' else 2 <= len(self.quiz_title) <= 100

    def is_quiz_descriptions_length_valid(self):
        return True if self.quiz_descriptions == '' else 10 <= len(self.quiz_descriptions) <= 2000

    def is_form_valid(self):
        if not self.is_quiz_title_taken() and \
            self.is_quiz_title_length_valid() and \
            self.is_quiz_descriptions_length_valid() and \
            self.quiz_complexity is not None:
            return True
        return False
