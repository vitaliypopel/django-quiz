# Generated by Django 5.0.7 on 2024-08-05 10:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('text', models.CharField(max_length=300)),
                ('is_last', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'questions',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('descriptions', models.CharField(max_length=2000)),
                ('url_title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Quizzes',
                'db_table': 'quizzes',
            },
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'users_session',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
            ],
            options={
                'db_table': 'choices',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz'),
        ),
        migrations.CreateModel(
            name='CompletedQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(default=0)),
                ('is_completed', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz')),
                ('user_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.usersession')),
            ],
            options={
                'verbose_name_plural': 'Completed quizzes',
                'db_table': 'user_completed_quizzes',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField(default=False)),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz')),
                ('user_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.usersession')),
            ],
            options={
                'db_table': 'user_answers',
            },
        ),
    ]
