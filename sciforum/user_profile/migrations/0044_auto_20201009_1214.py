# Generated by Django 3.1 on 2020-10-09 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0043_auto_20201009_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='postViews',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Views',
        ),
    ]