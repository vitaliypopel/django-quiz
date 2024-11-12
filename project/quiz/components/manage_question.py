from django_unicorn.components import UnicornView

from django.db import transaction
from django.shortcuts import redirect, reverse

from quiz.models import Quiz, Question, Choice


class ManageQuestionView(UnicornView):
    quiz: Quiz
    question: Question
    choices: list[Choice]

    questions: list[Question]

    latest_number: int

    number: int
    text: str
    variety: bool
    is_last: bool

    editing_mode = False

    def mount(self):
        self.set_data()

    def is_number_valid(self):
        return 1 <= int(self.number) <= 50 and \
            not self.questions.filter(number=self.number).exists() or \
            self.number == self.question.number

    def is_text_length_valid(self):
        return 2 <= len(self.text) <= 100

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

    def set_data(self):
        self.number = self.question.number
        self.text = self.question.text
        self.variety = self.question.variety
        self.is_last = self.question.is_last

        self.latest_number = self.number
        self.choices = Choice.objects.filter(
            question=self.question,
        )
        self.questions = Question.objects.filter(
            quiz=self.quiz,
        )

    def add_choice(self):
        Choice.objects.create(
            question=self.question,
            text='',
            is_correct=False,
        )
        self.set_data()

    def delete_choice(self, choice_pk: int):
        Choice.objects.get(pk=choice_pk).delete()
        self.set_data()

    def editing(self):
        self.set_data()
        self.editing_mode = not self.editing_mode

    def save_question(self):
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

            self.question.number = self.number
            self.question.text = ' '.join(self.text.split())
            self.question.variety = bool(self.variety)
            self.question.is_last = self.is_last
            self.question.save()

            for choice in self.choices:
                choice.save()

        if self.number != self.latest_number:
            return redirect(reverse(
                viewname='quiz:manage_quiz',
                args=(self.quiz.url_title,),
            ))

        self.editing()

    def delete_question(self):
        with transaction.atomic():
            Question.objects.get(
                quiz=self.quiz,
                number=self.number,
            ).delete()

            if self.is_last:
                for number in range(len(self.questions), 0, -1):
                    previous_question = Question.objects.filter(
                        quiz=self.quiz,
                        number=number,
                    )
                    if previous_question.exists():
                        previous_question = previous_question.first()
                        previous_question.is_last = True
                        previous_question.save()
                        break

        return redirect(reverse(
            viewname='quiz:manage_quiz',
            args=(self.quiz.url_title,),
        ))
