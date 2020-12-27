from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import os


class Post(models.Model):
    title = models.TextField()
    body = models.TextField()
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    viewCount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title


def get_image_filename(instance, filename):
    post_id = instance.id
    return os.path.join('%s/post_images' % post_id, filename)


class PostImages(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=get_image_filename, blank=True)


class Visitors(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    visitorIp = models.GenericIPAddressField(null=True, blank=True)
    visitDate = models.DateTimeField(blank=True)
