from django.urls import path

from . import views

app_name = 'matching'

urlpatterns = [
    path('matching/', views.matching_game, name='matching'),
    path('create_sentence/', views.create_sentence, name='create_sentence'),
    path('avoid_sentence/', views.avoid_sentence, name='avoid_sentence'),

]
