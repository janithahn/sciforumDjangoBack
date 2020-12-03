from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from enumfields import Enum
from enumfields import EnumField
from django.core.validators import MinValueValidator, MaxValueValidator


class UserRole(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    userRole = EnumField(UserRole, default=UserRole.USER, blank=True, null=True)
    aboutMe = models.TextField(max_length=500, blank=True)
    lastAccessDate = models.DateTimeField(auto_now=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    location = models.TextField(max_length=200, blank=True)
    login_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent_info = models.CharField(max_length=255, default='')
    postViews = models.IntegerField(blank=True, null=True)
    upVotes = models.IntegerField(blank=True, null=True)
    downVotes = models.IntegerField(blank=True, null=True)
    profileImg = models.ImageField(upload_to='profile_image', blank=True)
    # profileImgUrl = models.URLField(blank=True)


class UserContact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contact', primary_key=True)
    github = models.URLField(blank=True)
    linkedIn = models.URLField(blank=True)
    facebook = models.URLField(blank=True)


class UserLanguages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='languages')
    language = models.TextField(blank=True)


class UserEmployment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employment')
    position = models.TextField(blank=True)
    company = models.TextField(blank=True)
    start_year = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1969), MaxValueValidator(2051)])
    end_year = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1969), MaxValueValidator(2051)])
    currently_work = models.BooleanField(default=False)


class UserSkills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.TextField(blank=True)


class UserEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    school = models.TextField(blank=True)
    degree = models.CharField(blank=True, max_length=40)
    field_of_study = models.TextField(blank=True)
    start_year = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1969), MaxValueValidator(2051)])
    end_year = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1969), MaxValueValidator(2051)])
    description = models.TextField(blank=True)


'''class Views(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    postViews = models.IntegerField(blank=True, null=True)
    profileViews = models.IntegerField(blank=True, null=True)'''


class ProfileViewerInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    viewerUsername = models.TextField(null=True, blank=True)
    visitDate = models.DateTimeField(blank=True, null=True)
    viwer_ip = models.GenericIPAddressField(null=True, blank=True)
    viwer_agent_info = models.CharField(max_length=255, default='')


'''@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()'''

''''@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()'''


