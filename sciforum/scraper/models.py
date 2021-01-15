from djongo import models


class Events(models.Model):
    title = models.TextField()
    link = models.URLField()
    sentences = models.TextField()

    def __str__(self):
        return self.title


class Webinars(models.Model):
    link = models.URLField()
    texts = models.TextField()

    def __str__(self):
        return self.link
