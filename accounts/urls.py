from django.urls import path

from . import views

app_name = 'my'

urlpatterns = [
    path('add/', views.add_to_playlist, name='create_words'),
    path('playlists/', views.user_playlist, name='user_playlists'),
    path('playlist/my/game/<int:playlist_id>/', views.playlist_game, name='create_my_game'),
    path('playlist/create/', views.create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<uuid:playlist_uuid>/', views.playlist_detail, name='open_playlist'),
    path('remove_word_from_playlist/<int:playlist_id>/<int:word_id>/', views.remove_word_from_playlist,
         name='remove_word_from_playlist'),
    path('playlist/delete/<int:playlist_id>/', views.delete_playlist, name='delete_playlist'),


]