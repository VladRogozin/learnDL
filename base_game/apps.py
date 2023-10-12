from django.apps import AppConfig


class BaseGameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_game'
