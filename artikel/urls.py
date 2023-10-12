from django.urls import path

from . import views

app_name = 'artikel'

urlpatterns = [
    path('game/', views.artikel_game, name='artikel_game'),
    path('info/', views.artikel_info, name='artikel_info'),
]