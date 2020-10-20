# Generated by Django 3.1 on 2020-10-19 11:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('answer', '0001_initial'),
        ('vote', '0007_auto_20201019_1634'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answervote',
            unique_together={('answer', 'owner', 'voteType')},
        ),
    ]