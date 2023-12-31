from django.db import models
from django.contrib.auth.models import User


class Sentence(models.Model):
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('de', 'German'),
    )

    LEVEL_CHOICES = (
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    )

    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    text = models.TextField()
    translate = models.TextField(default="Нема")
    helpText = models.TextField(default="Нема")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='A1')
    photo = models.ImageField(upload_to='sentence_photos/', blank=True, null=True)
    hide = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class AvoidedSentence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentences = models.ManyToManyField(Sentence)

