from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BaseGameForms, WordComplaintForm, AvoidedWordForm
from django.contrib.auth.models import User

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import BaseGameModel, WordComplaint, AvoidedWord
from random import sample
from accounts.models import Playlist
from django.db.models import Q



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


@login_required
def user_words(request):
    words = BaseGameModel.objects.filter(autor=request.user)

    user_playlists = []
    if request.user.is_authenticated:
        user_playlists = Playlist.objects.filter(user=request.user)

    return render(request, 'base_game/my_words.html', {'words': words, 'user_playlists': user_playlists})


def game(request):

    # Получить доступные слова, где hide=False
    available_words = BaseGameModel.objects.filter(hide=False)

    # Получить предложения, которые нужно исключить из игры
    avoided_words = AvoidedWord.objects.filter(user=request.user).values('word')

    # Исключить предложения, которые содержатся в таблице AvoidedSentence
    available_words = available_words.exclude(pk__in=avoided_words)

    word = None
    options = []

    if available_words.count() > 0:
        word = sample(list(available_words), 1)[0]
        descriptions = sample(list(available_words.exclude(pk=word.pk)), 2)
        options = [word.description] + [desc.description for desc in descriptions]
        options = sample(options, len(options))

    return render(request, 'base_game/game_template.html', {'word': word, 'options': options})


def search_words(request):
    query = request.GET.get('q')
    if query:
        words = BaseGameModel.objects.filter(Q(word__icontains=query) & Q(hide=False))
    else:
        words = []

    # Инициализируйте пагинатор, указав количество элементов на странице
    paginator = Paginator(words, 10)  # В данном случае по 10 элементов на странице

    # Получите номер текущей страницы из запроса GET
    page_number = request.GET.get('page')

    # Получите объект Page для текущей страницы
    page = paginator.get_page(page_number)

    user_playlists = []
    if request.user.is_authenticated:
        user_playlists = Playlist.objects.filter(user=request.user)

    return render(request, 'base_game/search.html', {'page': page, 'user_playlists': user_playlists})


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


def avoid_word(request):
    if request.method == 'POST':
        word_id = request.POST.get('word_id')
        user_id = request.POST.get('user_id')

        user = User.objects.get(id=user_id)
        word = BaseGameModel.objects.get(id=word_id)

        avoided_word, created = AvoidedWord.objects.get_or_create(user=user)
        avoided_word.word.add(word)

        return redirect('words:game')

    else:
        form = AvoidedWordForm()

    return render(request, 'base_game/search.html', {'form': form})
