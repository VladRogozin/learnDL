from django.db import models
from django.contrib.auth.models import User
from base_game.models import BaseGameModel
import uuid


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    playlist_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class PlaylistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(BaseGameModel, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)