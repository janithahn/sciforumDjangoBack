# Generated by Django 3.0.5 on 2021-02-23 08:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mail_app', '0002_auto_20210222_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledmail',
            name='send_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 23, 8, 25, 47, 151763, tzinfo=utc)),
        ),
    ]