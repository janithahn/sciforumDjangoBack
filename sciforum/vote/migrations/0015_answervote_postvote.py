# Generated by Django 3.1 on 2020-10-20 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0016_auto_20201008_2015'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('answer', '0001_initial'),
        ('vote', '0014_auto_20201020_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voteType', models.CharField(choices=[('EMPTY', 'Empty'), ('LIKE', 'Like'), ('DISLIKE', 'Dislike')], default='EMPTY', max_length=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
            options={
                'unique_together': {('post', 'owner')},
            },
        ),
        migrations.CreateModel(
            name='AnswerVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voteType', models.CharField(choices=[('EMPTY', 'Empty'), ('LIKE', 'Like'), ('DISLIKE', 'Dislike')], default='EMPTY', max_length=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='answer.answer')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('answer', 'owner')},
            },
        ),
    ]