from django import forms

from .models import Playlist, Pages


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'description']


class CustomPagesForm(forms.ModelForm):
    class Meta:
        model = Pages
        fields = ['title', 'description', 'playlists']

    def __init__(self, user, *args, **kwargs):
        super(CustomPagesForm, self).__init__(*args, **kwargs)
        self.fields['playlists'].queryset = Playlist.objects.filter(user=user)

