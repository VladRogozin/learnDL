from django.db import models


class Word(models.Model):
    word_without_article = models.CharField(max_length=100)
    article = models.CharField(max_length=10)

    def __str__(self):
        return self.word_without_article

