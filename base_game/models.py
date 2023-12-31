from django.db import models
from django.contrib.auth.models import User


class BaseGameModel(models.Model):
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
    word = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    translate = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='baseGame_photos/', blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='A1')
    hide = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)




class WordComplaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(BaseGameModel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Жалоба от {self.user.username} на слово '{self.word.word}'"


class AvoidedWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ManyToManyField(BaseGameModel)