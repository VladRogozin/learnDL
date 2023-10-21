from django.urls import path

from . import views

app_name = 'my'

urlpatterns = [
    path('add/', views.add_to_playlist, name='add_to_playlist'),
    path('add/sentence/', views.add_to_playlist_sentences, name='add_to_playlist_sentences'),
    path('playlists/', views.user_playlist, name='user_playlists'),

    path('playlist/my/game/<int:playlist_id>/', views.playlist_games, name='create_my_game'),

    path('playlist/<int:playlist_id>/game/<str:game_type>/', views.playlist_game, name='playlist_game'),


    path('playlist/create/', views.create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<uuid:playlist_uuid>/', views.playlist_detail, name='open_playlist'),
    path('remove_word_from_playlist/<int:playlist_id>/<int:word_id>/', views.remove_word_from_playlist,
         name='remove_word_from_playlist'),
    path('remove_sentence_from_playlist/<int:playlist_id>/<int:sentence_id>/', views.remove_sentence_from_playlist,
         name='remove_sentence_from_playlist'),
    path('playlist/delete/<int:playlist_id>/', views.delete_playlist, name='delete_playlist'),
    path('toggle_word_visibility/<int:word_id>/<str:type>', views.toggle_word_visibility, name='toggle_word_visibility'),
    path('delete_word/<int:word_id>/<str:type>/', views.delete_word, name='delete_word'),
]