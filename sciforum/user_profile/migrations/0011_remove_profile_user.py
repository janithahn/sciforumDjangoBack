# Generated by Django 3.1 on 2020-09-27 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0010_auto_20200927_0911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
    ]