# Generated by Django 3.1 on 2020-12-03 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0066_auto_20201203_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usereducation',
            name='degree',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]