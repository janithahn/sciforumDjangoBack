# Generated by Django 3.1 on 2020-12-12 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0020_delete_answercommentvote'),
        ('comment', '0002_auto_20201207_1941'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AnswerComment',
        ),
    ]