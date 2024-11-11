# Generated by Django 5.1.2 on 2024-11-08 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quiz_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='variety',
            field=models.BooleanField(choices=[(True, 'Single choice'), (False, 'Multiple choices')]),
        ),
    ]