from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from random import sample

from .forms import AvoidedArticleForm
from .models import Word, AvoidedArticle


def artikel_info(request):
    return render(request, 'artikel/artikel_info.html')


def artikel_game(request):
    user = request.user  # Получаем текущего пользователя (предполагается, что пользователь авторизован)

    # Получаем список всех избегаемых артиклей для текущего пользователя
    avoided_articles = AvoidedArticle.objects.filter(user=user).values_list('word__article', flat=True)

    # Получаем доступные слова, исключая те, которые содержат избегаемые артикли
    available_words = Word.objects.exclude(article__in=avoided_articles)

    # Если доступных слов больше 0, выбираем одно случайное слово из них
    if available_words.count() > 0:
        word = sample(list(available_words), 1)[0]
        articles = sample(list(Word.objects.exclude(pk=word.pk)), 3)
        options = [word.article] + [article.article for article in articles]
        options = sample(options, len(options))
    else:
        # Если нет доступных слов, можно вернуть сообщение о том, что игра закончена, либо другое действие по вашему выбору.
        # В данном случае, мы просто создаем пустой список options.
        options = []

    context = {
        'word': word, # здесь используется поле без артикля
        'options': options,
        'article': word.article,  # добавляем артикль как строку
    }

    return render(request, 'artikel/artikel_game.html', context)


def avoid_article(request):
    if request.method == 'POST':
        word_id = request.POST.get('word_id')
        user_id = request.POST.get('user_id')

        user = User.objects.get(id=user_id)
        word = Word.objects.get(id=word_id)

        avoided_word, created = AvoidedArticle.objects.get_or_create(user=user)
        avoided_word.word.add(word)

        return redirect('artikel:artikel_game')

    else:
        form = AvoidedArticleForm()

    return render(request, 'base_game/search.html', {'form': form})