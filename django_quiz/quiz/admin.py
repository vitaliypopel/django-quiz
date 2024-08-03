from django.contrib import admin

from . import models

m = (
    models.Quiz,
    models.Question,
    models.Choice,
    models.UserSession,
    models.Answer,
    models.CompletedQuiz,
)

for model in m:
    admin.site.register(model)
