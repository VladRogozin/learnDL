from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import PlaylistForm, CustomPagesForm
from .models import PlaylistItem, Playlist, Pages, SavedPage
from base_game.models import BaseGameModel
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from matching.models import Sentence
from django.contrib import messages


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
    return redirect('my:create_playlist')


@login_required
def add_to_playlist_sentences(request):
    if request.user.is_authenticated and request.method == 'POST':
        word_id = request.POST.get('word_id')
        playlist_id = request.POST.get('playlist')
        word = Sentence.objects.get(pk=word_id)
        playlist = Playlist.objects.get(pk=playlist_id)
        playlist_item = PlaylistItem(user=request.user, sentence=word, playlist=playlist)
        playlist_item.save()
    return redirect('my:create_playlist')

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
    playlists = Playlist.objects.filter(user=request.user)

    words = list(reversed(BaseGameModel.objects.filter(autor=request.user).order_by('created_at')))
    paginator_words = Paginator(words, 10)
    page_number_words = request.GET.get('page_words')
    page_words = paginator_words.get_page(page_number_words)

    sentences = list(reversed(Sentence.objects.filter(autor=request.user).order_by('created_at')))
    paginator_sentences = Paginator(sentences, 10)
    page_number_sentences = request.GET.get('page_sentences')
    page_sentences = paginator_sentences.get_page(page_number_sentences)

    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            new_playlist = form.save(commit=False)
            new_playlist.user = request.user
            new_playlist.save()
            return redirect('my:playlist_detail', playlist_id=new_playlist.id)
    else:
        form = PlaylistForm()

    user_playlists = []
    if request.user.is_authenticated:
        user_playlists = Playlist.objects.filter(user=request.user)

    return render(request, 'playlist/create_playlist.html', {
        'form': form,
        'playlists': playlists,
        'page_words': page_words,
        'user_playlists': user_playlists,
        'page_sentences': page_sentences,
    })


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


def playlist_game(request, playlist_id, game_type):

    if game_type == 'matching':
        playlist_id = playlist_id
        return render(request, 'matching/new_sentences_game.html', {'playlist_id': playlist_id})

    elif game_type == 'base_game':
        playlist_id = playlist_id
        return render(request, 'base_game/new_game.html', {'playlist_id': playlist_id})

    else:
        return HttpResponse("Неверный тип игры")


# В представлении playlist_games
def playlist_games(request, playlist_id):
    playlist = None
    playlist_items = None

    if playlist_id:
        playlist = get_object_or_404(Playlist, id=playlist_id)
        playlist_items = PlaylistItem.objects.filter(playlist=playlist)

    return render(request, 'playlist/ALL.html', {'playlist': playlist, 'playlist_items': playlist_items})


def remove_word_from_playlist(request, playlist_id, word_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    word = get_object_or_404(BaseGameModel, id=word_id)

    # Перевірте, чи слово дійсно належить до цього плейлиста
    playlist_item = PlaylistItem.objects.filter(playlist=playlist, word=word).first()
    if playlist_item:
        playlist_item.delete()

    return redirect('my:playlist_detail', playlist_id=playlist_id)


def remove_sentence_from_playlist(request, playlist_id, sentence_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    sentence = get_object_or_404(Sentence, id=sentence_id)

    # Перевірте, чи слово дійсно належить до цього плейлиста
    playlist_item = PlaylistItem.objects.filter(playlist=playlist, sentence=sentence).first()
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


def toggle_word_visibility(request, word_id, type):

    if type == 'word':
        if request.method == 'POST':
            word = BaseGameModel.objects.get(pk=word_id)
            word.hide = not word.hide  # Инвертировать видимость слова
            word.save()
            return JsonResponse({'hide': word.hide})

    if type == 'sentence':
        if request.method == 'POST':
            word = Sentence.objects.get(pk=word_id)
            word.hide = not word.hide  # Инвертировать видимость слова
            word.save()
            return JsonResponse({'hide': word.hide})


@login_required
def delete_word(request, word_id, type):

    if type == 'word':
        word = BaseGameModel.objects.get(id=word_id)
        if word.autor == request.user:
            word.delete()
            messages.success(request, 'Слово успешно удалено.')
        else:
            messages.error(request, 'Вы не являетесь автором этого слова.')
    elif type == 'sentences':
        sentence = Sentence.objects.get(id=word_id)
        if sentence.autor == request.user:
            sentence.delete()
            messages.success(request, 'Слово успешно удалено.')
        else:
            messages.error(request, 'Вы не являетесь автором этого слова.')

    return redirect('my:create_playlist')


def view_page(request, page_id):
    page = get_object_or_404(Pages, pk=page_id)
    return render(request, 'page/page.html', {'page': page})


def view_all_pages(request):
    pages = Pages.objects.filter(user=request.user)
    saved_pages = SavedPage.objects.filter(user=request.user)
    return render(request, 'page/all_pages.html', {'pages': pages, 'saved_pages': saved_pages})


def create_pages(request):
    if request.method == 'POST':
        form = CustomPagesForm(request.user, request.POST)
        if form.is_valid():
            new_page = form.save(commit=False)
            new_page.user = request.user
            new_page.save()
            form.save_m2m()
            return redirect('my:view_all_pages')
    else:
        form = CustomPagesForm(request.user)

    return render(request, 'page/create_pages.html', {'form': form})


def delete_page(request, page_id):
    page = get_object_or_404(Pages, pk=page_id)

    if request.user.id == page.user.id:
        try:
            page.delete()
            return JsonResponse({'message': 'Успешно удалено', 'status': 'success'})
        except Exception as e:
            return JsonResponse({'message': f'Ошибка при удалении: {str(e)}', 'status': 'error'})

    return JsonResponse({'message': 'Щось не так!', 'status': 'error'})


def save_page(request, page_id):
    page = get_object_or_404(Pages, pk=page_id)

    # Попытайтесь получить или создать объект SavedPage для пользователя и страницы
    saved_page, created = SavedPage.objects.get_or_create(user=request.user, page=page)

    if created:
        # Если объект был создан (то есть страница ранее не была сохранена), сохраните его
        saved_page.save()
        # Опционально, вы можете добавить сообщение об успешном сохранении

    return redirect('my:view_page', page_id=page_id)

