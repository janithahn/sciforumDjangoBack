# Generated by Django 3.0.5 on 2021-02-04 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_postimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='label',
            field=models.CharField(choices=[('CS', 'Cs'), ('STAT', 'Stat'), ('MATHEMATICS', 'Mathematics'), ('PHYSICS', 'Physics'), ('CHEMISTRY', 'Chemistry'), ('ZOOLOGY', 'Zoology'), ('BOTANY', 'Botany'), ('ES', 'Es'), ('OTHER', 'Other')], default='OTHER', max_length=20),
        ),
    ]