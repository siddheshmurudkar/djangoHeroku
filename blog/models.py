# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
# Importing to sublclass(inheriting) models
# Create your models here.
class Feed(models.Model):
    title = models.CharField(max_length=50)
    url=models.URLField()

# To return a user readable name
    def __str__(self):
        return self.title


class Article(models.Model):
    title=models.CharField(max_length=50)
    url=models.URLField()
    publication_date = models.DateTimeField()
    description=models.CharField(max_length=200)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

     #Delete all the article objects if the corresponding feed is deleted(one to many relationship)

    def __str__(self):
        return self.title
