# Generated by Django 3.0.5 on 2021-02-04 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='label',
            field=models.CharField(blank=True, choices=[('CS', 'Cs'), ('STAT', 'Stat'), ('MATHEMATICS', 'Mathematics'), ('PHYSICS', 'Physics'), ('CHEMISTRY', 'Chemistry'), ('ZOOLOGY', 'Zoology'), ('BOTANY', 'Botany'), ('ES', 'Es'), ('OTHER', 'Other')], max_length=20),
        ),
    ]
