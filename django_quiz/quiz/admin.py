from django.contrib import admin

from . import models

admin.site.register(
    models.Quiz,
    models.Question,
    models.Choice,
    models.UserAnswer,
)
