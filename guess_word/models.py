from django.db import models


class GuessWord(models.Model):
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

    guess_word = models.CharField(max_length=200, default="Нема")
    help_words = models.CharField(max_length=200, default="Нема")
    photo = models.ImageField(upload_to='guess_word_image/', blank=True, null=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='A1')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)