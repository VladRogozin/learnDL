from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
import random

from .forms import SentenceForm, AvoidedSentenceForm
from .models import Sentence, AvoidedSentence


def matching_game(request):
    sentences = Sentence.objects.filter(hide=False)

    if request.user.is_authenticated:
        avoided_sentences = AvoidedSentence.objects.filter(user=request.user).values('sentences')

        sentences = sentences.exclude(pk__in=avoided_sentences)


    random_sentence = None
    sentences_id = None
    if sentences:
        random_sentence = random.choice(sentences)
        sentences_id = random_sentence
        random_sentence = random_sentence.text

    context = {'random_sentence': random_sentence, 'sentences_id': sentences_id}
    return render(request, 'matching/matching_game.html', context)


@login_required
def create_sentence(request):
    if request.method == 'POST':
        form = SentenceForm(request.POST, request.FILES)
        if form.is_valid():
            sentence = form.save(commit=False)
            sentence.autor = request.user  # Привязать автора к пользователю
            sentence.save()
            return redirect('matching:create_sentence')  # Перенаправить на страницу списка предложений
    else:
        form = SentenceForm()
    return render(request, 'matching/create_matching.html', {'form': form})


def avoid_sentence(request):
    if request.method == 'POST':
        word_id = request.POST.get('sentences_id')
        user_id = request.POST.get('user_id')

        user = User.objects.get(id=user_id)
        sentences = Sentence.objects.get(id=word_id)

        avoided_sentence, created = AvoidedSentence.objects.get_or_create(user=user)
        avoided_sentence.sentences.add(sentences)

        return redirect('matching:matching')

    else:
        form = AvoidedSentenceForm()

    return render(request, 'base_game/search.html', {'form': form})


def new_sentences_game(request):
    return render(request, 'matching/new_sentences_game.html', )


def new_sentences_game_new(request, playlist):
    descriptions = Sentence.objects.filter(playlistitem__playlist=playlist).values('text', 'translate', 'helpText', 'photo',)
    phrases = list(descriptions)

    return JsonResponse({'phrases': phrases}, safe=False)
