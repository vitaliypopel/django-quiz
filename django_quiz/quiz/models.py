from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=2000)
    url_title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quizzes'

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    number = models.IntegerField()
    text = models.CharField(max_length=300)

    class Meta:
        db_table = 'questions'

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField()

    class Meta:
        db_table = 'choices'

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    session = models.CharField(max_length=300)

    class Meta:
        db_table = 'user_answers'
