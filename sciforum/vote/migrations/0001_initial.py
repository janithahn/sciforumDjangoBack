# Generated by Django 3.1 on 2020-10-19 02:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import vote.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0016_auto_20201008_2015'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voteType', enumfields.fields.EnumField(blank=True, default='EMPTY', enum=vote.models.VoteType, max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]