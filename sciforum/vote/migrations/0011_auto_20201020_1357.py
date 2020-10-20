# Generated by Django 3.1 on 2020-10-20 08:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_auto_20201008_2015'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0010_auto_20201020_1356'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postvote',
            unique_together={('post', 'owner')},
        ),
    ]