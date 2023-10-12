from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BaseGameForms, WordComplaintForm

from django.shortcuts import render
from .models import BaseGameModel, WordComplaint
from random import sample
from accounts.models import Playlist


@login_required
def create_words(request):
    if request.method == 'POST':
        form = BaseGameForms(request.POST)
        if form.is_valid():
            word_instance = form.save(commit=False)
            word_instance.autor = request.user
            word_instance.save()
            return redirect('words:create_words')
    else:
        form = BaseGameForms()

    # Если форма не прошла валидацию, передайте ошибки в контекст
    errors = form.errors if form.errors else None

    return render(request, 'base_game/create_word.html', {'form': form, 'errors': errors})


def game(request):
    words = list(BaseGameModel.objects.all())
    word = sample(words, 1)[0] # take random word
    descriptions = sample(list(BaseGameModel.objects.exclude(pk=word.pk)), 2)
    options = [word.description] + [desc.description for desc in descriptions]
    options = sample(options, len(options))

    return render(request, 'base_game/game_template.html', {'word': word, 'options': options})


def search_words(request):
    query = request.GET.get('q')
    if query:
        words = BaseGameModel.objects.filter(word__icontains=query)
    else:
        words = []

    user_playlists = []
    if request.user.is_authenticated:
        user_playlists = Playlist.objects.filter(user=request.user)

    return render(request, 'base_game/search.html', {'words': words, 'user_playlists': user_playlists})


def complain_word(request, word_id):
    word = get_object_or_404(BaseGameModel, id=word_id)

    if request.method == 'POST':
        form = WordComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.word = word
            complaint.save()

            # Проверяем, сколько жалоб было отправлено для данного слова
            complaints_count = WordComplaint.objects.filter(word=word).count()

            if complaints_count > 2:
                word.delete()  # Удаляем слово, если количество жалоб больше 2

            return redirect('words:game')  # Замените 'word_list' на URL-путь к списку слов
    else:
        form = WordComplaintForm()

    return render(request, 'complaint_form.html', {'form': form, 'word': word})


