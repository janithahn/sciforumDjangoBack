# Generated by Django 3.1 on 2020-10-20 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0011_auto_20201020_1357'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answervote',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='postvote',
            unique_together=set(),
        ),
    ]