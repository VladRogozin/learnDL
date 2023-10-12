from django.urls import path

from . import views

app_name = 'words'

urlpatterns = [
    path('create/', views.create_words, name='create_words'),
    path('game/', views.game, name='game'),
    path('search/', views.search_words, name='search_words'),
    path('complain/<int:word_id>/', views.complain_word, name='complain_word'),


]
