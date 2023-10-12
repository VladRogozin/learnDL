from django.shortcuts import render
from random import sample
from .models import Word


def artikel_game(request):
    words = list(Word.objects.all())
    word = sample(words, 1)[0] # выбираем случайное слово
    articles = sample(list(Word.objects.exclude(pk=word.pk)), 3) # выбираем 3 случайных артикля
    options = [word.article] + [article.article for article in articles] # создаем список вариантов ответа
    options = sample(options, len(options)) # перемешиваем варианты ответов

    context = {
        'word': word, # здесь используется поле без артикля
        'options': options,
        'article': word.article,  # добавляем артикль как строку
    }

    return render(request, 'artikel/artikel_game.html', context)


def artikel_info(request):
    return render(request, 'artikel/artikel_info.html')