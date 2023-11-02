from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Playlist, Pages
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 4:
            raise forms.ValidationError('Логін повинен містити не менше 4 символів.')
        if not re.match('^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError('Логін може містити тільки букви та цифри латинського алфавіту.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 4:
            raise forms.ValidationError('Пароль має містити щонайменше 4 символи.')
        return password1


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'description']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if not title:
            self.add_error('title', 'Назва не заповнена.')

        if not description:
            self.add_error('description', 'Опис не заповнена.')

        return cleaned_data


class CustomPagesForm(forms.ModelForm):
    class Meta:
        model = Pages
        fields = ['title', 'description', 'playlists']

    def __init__(self, user, *args, **kwargs):
        super(CustomPagesForm, self).__init__(*args, **kwargs)
        self.fields['playlists'].queryset = Playlist.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        playlists = cleaned_data.get('playlists')

        if not title:
            self.add_error('title', 'Назва не заповнена.')

        if not playlists:
            self.add_error('playlists', 'У вас не вибрано жодного плейлиста.')

        return cleaned_data

