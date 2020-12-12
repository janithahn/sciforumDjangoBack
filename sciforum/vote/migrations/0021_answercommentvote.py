# Generated by Django 3.1 on 2020-12-12 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0004_answercomment'),
        ('vote', '0020_delete_answercommentvote'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerCommentVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voteType', models.CharField(choices=[('EMPTY', 'Empty'), ('LIKE', 'Like'), ('DISLIKE', 'Dislike')], default='EMPTY', max_length=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comment.answercomment')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('comment', 'owner')},
            },
        ),
    ]
