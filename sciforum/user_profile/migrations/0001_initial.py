# Generated by Django 3.0.5 on 2021-01-28 07:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import user_profile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('userRole', enumfields.fields.EnumField(blank=True, default='USER', enum=user_profile.models.UserRole, max_length=10, null=True)),
                ('aboutMe', models.TextField(blank=True, max_length=500)),
                ('lastAccessDate', models.DateTimeField(auto_now=True)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('location', models.TextField(blank=True, max_length=200)),
                ('login_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent_info', models.CharField(default='', max_length=255)),
                ('postViews', models.IntegerField(blank=True, null=True)),
                ('upVotes', models.IntegerField(blank=True, null=True)),
                ('downVotes', models.IntegerField(blank=True, null=True)),
                ('profileImg', models.ImageField(blank=True, upload_to='profile_image')),
            ],
        ),
        migrations.CreateModel(
            name='UserContact',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='contact', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('github', models.URLField(blank=True)),
                ('linkedIn', models.URLField(blank=True)),
                ('facebook', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLanguages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserEmployment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.TextField(blank=True)),
                ('company', models.TextField(blank=True)),
                ('start_year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1969), django.core.validators.MaxValueValidator(2051)])),
                ('end_year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1969), django.core.validators.MaxValueValidator(2051)])),
                ('currently_work', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.TextField(blank=True)),
                ('degree', models.CharField(blank=True, max_length=40)),
                ('field_of_study', models.TextField(blank=True)),
                ('start_year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1969), django.core.validators.MaxValueValidator(2051)])),
                ('end_year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1969), django.core.validators.MaxValueValidator(2051)])),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileViewerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewerUsername', models.TextField(blank=True, null=True)),
                ('visitDate', models.DateTimeField(blank=True, null=True)),
                ('viwer_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('viwer_agent_info', models.CharField(default='', max_length=255)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]