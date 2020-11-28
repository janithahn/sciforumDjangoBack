# Generated by Django 3.1 on 2020-11-28 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('user_profile', '0054_delete_usercontact'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserContact',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='contact', serialize=False, to='auth.user')),
                ('github', models.URLField(blank=True)),
                ('linkedIn', models.URLField(blank=True)),
                ('facebook', models.URLField(blank=True)),
            ],
        ),
    ]