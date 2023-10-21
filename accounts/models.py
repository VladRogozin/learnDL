from django.db import models
from django.contrib.auth.models import User
from base_game.models import BaseGameModel
from artikel.models import Word
from matching.models import Sentence
import uuid


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    playlist_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PlaylistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(BaseGameModel, on_delete=models.CASCADE, null=True)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, null=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

