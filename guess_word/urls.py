from django.urls import path

from . import views

app_name = 'guess'

urlpatterns = [
    path('guess/', views.guess_list, name='guess_list'),
    path('guess/game/', views.guess_game, name='guess_game'),
]
