# Generated by Django 3.1 on 2020-11-28 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0049_auto_20201128_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserContact',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='userContact', serialize=False, to='user_profile.profile')),
                ('github', models.URLField(blank=True)),
                ('linkedIn', models.URLField(blank=True)),
                ('facebook', models.URLField(blank=True)),
            ],
        ),
    ]
