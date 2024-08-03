from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=2000)
    url_title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Quizzes'
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


class UserSession(models.Model):
    session = models.CharField(max_length=300)

    class Meta:
        db_table = 'users_session'

    def __str__(self):
        return self.session


class Answer(models.Model):
    user_session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

    class Meta:
        db_table = 'user_answers'


class CompletedQuiz(models.Model):
    user_session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    is_completed = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Completed quizzes'
        db_table = 'user_completed_quizzes'
