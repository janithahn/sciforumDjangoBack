# Generated by Django 3.1 on 2020-10-09 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0037_profile_userrole'),
    ]

    operations = [
        migrations.CreateModel(
            name='Views',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_profile.profile')),
                ('postViews', models.IntegerField(blank=True, null=True)),
                ('profileViews', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='views',
        ),
    ]