# Generated by Django 3.0.5 on 2021-01-17 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_webinar_reference_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinar',
            name='title',
            field=models.TextField(default=''),
        ),
    ]