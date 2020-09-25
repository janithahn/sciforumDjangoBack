from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aboutMe = models.TextField(max_length=500, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    lastAccessDate = models.DateTimeField()
    profileImgUrl = models.URLField(max_length=200, blank=True)
    views = models.IntegerField(null=True, blank=True)
    upVotes = models.IntegerField(null=True, blank=True)
    downVotes = models.IntegerField(null=True, blank=True)
    facebook = models.URLField(blank=True)
    linkedIn = models.URLField(blank=True)
    github = models.URLField(blank=True)

    def __str__(self):
        return self.user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()