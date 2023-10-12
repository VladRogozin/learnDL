from random import sample
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import PlaylistForm
from .models import PlaylistItem, Playlist
from base_game.models import BaseGameModel
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base_view')  # Замените 'home' на URL вашей главной страницы
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def add_to_playlist(request):
    if request.user.is_authenticated and request.method == 'POST':
        word_id = request.POST.get('word_id')
        playlist_id = request.POST.get('playlist')
        word = BaseGameModel.objects.get(pk=word_id)
        playlist = Playlist.objects.get(pk=playlist_id)
        playlist_item = PlaylistItem(user=request.user, word=word, playlist=playlist)
        playlist_item.save()
    return redirect('base_view')


@login_required
def user_playlist(request):
    # Получите текущего пользователя
    user = request.user

    # Получите все слова в плейлисте текущего пользователя
    saved_words = PlaylistItem.objects.filter(user=user)

    context = {'saved_words': saved_words}
    return render(request, 'registration/my_playlist.html', context)


@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            new_playlist = form.save(commit=False)
            new_playlist.user = request.user
            new_playlist.save()
            return redirect('my:playlist_detail', playlist_id=new_playlist.id)
    else:
        form = PlaylistForm()

    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'playlist/create_playlist.html', {'form': form, 'playlists': playlists})


@login_required
def playlist_detail(request, playlist_id=None, playlist_uuid=None):
    playlist = None
    playlist_items = None

    if playlist_id:
        playlist = get_object_or_404(Playlist, id=playlist_id)
        playlist_items = PlaylistItem.objects.filter(playlist=playlist)
    elif playlist_uuid:
        playlist = get_object_or_404(Playlist, playlist_uuid=playlist_uuid)
        playlist_items = PlaylistItem.objects.filter(playlist=playlist)

    return render(request, 'playlist/playlist_detail.html', {'playlist': playlist, 'playlist_items': playlist_items})


@login_required
def playlist_game(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    playlist_items = PlaylistItem.objects.filter(playlist=playlist)

    words = [item.word for item in playlist_items]

    if len(words) < 3:
        return HttpResponse("Плейлист має містити щонайменше 3 слова для гри.")

    word = sample(words, 1)[0]
    descriptions = sample(list(BaseGameModel.objects.filter(~Q(pk=word.pk)).filter(pk__in=[w.pk for w in words])), 2)
    options = [word.description] + [desc.description for desc in descriptions]
    options = sample(options, len(options))

    return render(request, 'base_game/game_template.html', {'word': word, 'options': options})


def remove_word_from_playlist(request, playlist_id, word_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    word = get_object_or_404(BaseGameModel, id=word_id)

    # Перевірте, чи слово дійсно належить до цього плейлиста
    playlist_item = PlaylistItem.objects.filter(playlist=playlist, word=word).first()
    if playlist_item:
        playlist_item.delete()

    return redirect('my:playlist_detail', playlist_id=playlist_id)

def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)

    # Видалення всіх пов'язаних слів
    PlaylistItem.objects.filter(playlist=playlist).delete()

    # Видалення плейлиста
    playlist.delete()

    return redirect('my:create_playlist')

