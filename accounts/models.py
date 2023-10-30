from django.db import models
from django.contrib.auth.models import User
from base_game.models import BaseGameModel

from matching.models import Sentence
import uuid


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100, default='', null=True)
    playlist_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PlaylistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(BaseGameModel, on_delete=models.CASCADE, null=True)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, null=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Pages(models.Model):
    title = models.CharField(max_length=100, default='')
    description = models.TextField(max_length=100, default='', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlists = models.ManyToManyField(Playlist)

    def __str__(self):
        return f"{self.title}  : {self.description}"


class SavedPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Pages, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s saved page: {self.page.title}"

