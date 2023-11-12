from random import sample

from django.shortcuts import render
from .models import GuessWord


def guess_list(request):
    words = GuessWord.objects.all()
    return render(request, 'guess_word/all_guess_words.html', {'words': words})


def guess_game(request):
    all_words = GuessWord.objects.all()

    random_words = [
        {
            'guess_word': word.guess_word,
            'help_words': word.help_words,
            'photo_url': word.photo.url if word.photo else None,
        }
        for word in sample(list(all_words), 10)
    ]

    return render(request, 'guess_word/guess_game.html', {'words': random_words})
