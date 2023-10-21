from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    word_without_article = models.CharField(max_length=100)
    article = models.CharField(max_length=10)

    def __str__(self):
        return self.word_without_article


class AvoidedArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ManyToManyField(Word)

