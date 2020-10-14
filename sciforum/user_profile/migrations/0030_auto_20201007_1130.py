# Generated by Django 3.1 on 2020-10-07 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0029_profile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='login_ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_agent_info',
            field=models.CharField(default='', max_length=255),
        ),
    ]