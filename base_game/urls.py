from django.urls import path

from . import views

app_name = 'words'

urlpatterns = [
    path('create/', views.create_words, name='create_words'),
    path('game/', views.game, name='game'),
    path('search/', views.search_words, name='search_words'),
    path('complain/<int:word_id>/', views.complain_word, name='complain_word'),
    path('avoid_word/', views.avoid_word, name='avoid_word'),
    path('user_words/', views.user_words, name='user_words'),

]
