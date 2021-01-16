from djongo import models


class Event(models.Model):
    title = models.TextField()
    link = models.URLField()
    sentences = models.TextField()

    def __str__(self):
        return self.title


class Webinar(models.Model):
    link = models.URLField()
    texts = models.TextField()

    def __str__(self):
        return self.link
