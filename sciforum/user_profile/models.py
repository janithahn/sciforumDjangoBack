from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from enumfields import Enum
from enumfields import EnumField

class UserRole(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    userRole = EnumField(UserRole, default=UserRole.USER, blank=True, null=True)
    aboutMe = models.TextField(max_length=500, blank=True)
    lastAccessDate = models.DateTimeField(auto_now=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    location = models.TextField(max_length=200, blank=True)
    login_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent_info = models.CharField(max_length=255, default='')
    views = models.IntegerField(blank=True, null=True)
    upVotes = models.IntegerField(blank=True, null=True)
    downVotes = models.IntegerField(blank=True, null=True)
    profileImg = models.ImageField(upload_to='profile_image', blank=True)
    #profileImgUrl = models.URLField(blank=True)

class UserContact(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    github = models.URLField(blank=True)
    linkedIn = models.URLField(blank=True)
    facebook = models.URLField(blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

''''@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()'''


