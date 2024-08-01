from django.contrib import admin

from . import models

m = (
    models.Quiz,
    models.Question,
    models.Choice,
    models.UserAnswer,
)

for model in m:
    admin.site.register(model)
