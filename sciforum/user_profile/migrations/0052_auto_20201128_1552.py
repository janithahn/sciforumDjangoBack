# Generated by Django 3.1 on 2020-11-28 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0051_auto_20201128_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercontact',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_profile.profile'),
        ),
    ]
