from django_unicorn.components import UnicornView

from django.db import transaction
from django.shortcuts import redirect, reverse

from quiz.models import Quiz, Question


class CreateQuestionView(UnicornView):
    quiz: Quiz
    questions: list[Question]

    number = 1
    text = ''
    variety = None
    is_last = False

    creating_mode = False

    def mount(self):
        self.set_default_data()

    def is_number_valid(self):
        return 1 <= int(self.number) <= 50 and \
            not self.questions.filter(number=self.number).exists()

    def is_text_length_valid(self):
        return 10 <= len(self.text) <= 300

    def is_form_valid(self):
        if self.variety is not None and \
            self.is_number_valid() and \
            self.is_text_length_valid():
            return True
        return False

    def get_data(self):
        return {
            'number': self.number,
            'text': ' '.join(self.text.split()),
            'variety': self.variety,
            'is_last': self.is_last,
        }

    def set_default_data(self):
        self.number = 1
        self.text = ''
        self.variety = None
        self.is_last = False
        self.questions = Question.objects.filter(
            quiz=self.quiz,
        )

    def creating(self):
        self.set_default_data()
        self.creating_mode = not self.creating_mode

    def create_question(self):
        if not self.is_form_valid():
            return None

        with transaction.atomic():
            last_question = Question.objects.filter(
                quiz=self.quiz,
                is_last=True,
            )
            if self.is_last and last_question.exists():
                last_question = last_question.first()
                last_question.is_last = False
                last_question.save()

            Question.objects.create(
                quiz=self.quiz,
                **self.get_data(),
            )

        return redirect(reverse(
            viewname='quiz:manage_quiz',
            args=(self.quiz.url_title,),
        ))
