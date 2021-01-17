from djongo import models
from datetime import datetime


class Event(models.Model):
    title = models.TextField()
    link = models.URLField()
    sentences = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Webinar(models.Model):
    link = models.URLField()
    title = models.TextField(default='')
    texts = models.TextField()
    reference_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link
