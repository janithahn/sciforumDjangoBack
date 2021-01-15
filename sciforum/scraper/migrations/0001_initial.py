# Generated by Django 3.0.5 on 2021-01-15 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('link', models.URLField()),
                ('sentences', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Webinars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('texts', models.TextField()),
            ],
        ),
    ]
