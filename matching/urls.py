from django.urls import path

from . import views

app_name = 'matching'

urlpatterns = [
    path('matching/', views.matching_game, name='matching'),
    path('create_sentence/', views.create_sentence, name='create_sentence'),
    path('avoid_sentence/', views.avoid_sentence, name='avoid_sentence'),
    path('new_sentences_game/', views.new_sentences_game, name='new_sentences_game'),
    path('new_sentences_game_new/<int:playlist>/', views.new_sentences_game_new, name='new_sentences_game_new'),
]
