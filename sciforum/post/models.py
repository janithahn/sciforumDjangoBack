from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewCount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Visitors(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    visitorIp = models.GenericIPAddressField(null=True, blank=True)
    visitDate = models.DateTimeField(blank=True)
