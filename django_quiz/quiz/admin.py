from django.contrib import admin

from . import models

quiz_models = (
    models.Quiz,
    models.Question,
    models.Choice,
    models.UserSession,
    models.Answer,
    models.CompletedQuiz,
)

for model in quiz_models:
    admin.site.register(model)
