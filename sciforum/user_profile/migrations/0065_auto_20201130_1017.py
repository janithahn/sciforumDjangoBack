# Generated by Django 3.1 on 2020-11-30 04:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0064_auto_20201129_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usereducation',
            name='field_of_study',
            field=models.TextField(blank=True, validators=[django.core.validators.MinValueValidator(1969), django.core.validators.MaxValueValidator(2051)]),
        ),
        migrations.AlterField(
            model_name='usereducation',
            name='start_year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1969), django.core.validators.MaxValueValidator(2051)]),
        ),
        migrations.AlterField(
            model_name='useremployment',
            name='end_year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1969), django.core.validators.MaxValueValidator(2051)]),
        ),
        migrations.AlterField(
            model_name='useremployment',
            name='start_year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1969), django.core.validators.MaxValueValidator(2051)]),
        ),
    ]
