# Generated by Django 3.0.5 on 2021-02-22 11:39

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailRecipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_address', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledMail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=40)),
                ('template', models.FileField(upload_to='')),
                ('send_on', models.DateTimeField(default=datetime.datetime(2021, 2, 22, 11, 39, 48, 927758, tzinfo=utc))),
                ('recipients_list', models.ManyToManyField(related_name='mail_list', to='mail_app.MailRecipient')),
            ],
        ),
        migrations.CreateModel(
            name='MailAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment_file', models.FileField(upload_to='')),
                ('attached_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='mail_app.ScheduledMail')),
            ],
        ),
    ]
