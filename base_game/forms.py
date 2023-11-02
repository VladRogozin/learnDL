from django import forms
from .models import BaseGameModel, WordComplaint
from .models import AvoidedWord
from django.core.exceptions import ValidationError
from PIL import Image


class BaseGameForms(forms.ModelForm):
    class Meta:
        model = BaseGameModel
        fields = ['language', 'word', 'description', 'translate', 'photo', 'autor', 'level', 'hide']

    level = forms.ChoiceField(choices=BaseGameModel.LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    language = forms.ChoiceField(choices=BaseGameModel.LANGUAGE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        word = cleaned_data.get('word')
        description = cleaned_data.get('description')

        if not word:
            self.add_error('word', 'Це поле обов\'язкове для заповнення.')

        if not description:
            self.add_error('description', 'Це поле обов\'язкове для заповнення.')

        return cleaned_data

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if photo:
            # Открываем изображение с использованием Pillow
            try:
                image = Image.open(photo)
            except Exception as e:
                raise ValidationError('Неможливо відкрити зображення.')

            # Проверка размера изображения
            max_width = 1100
            max_height = 1100
            if image.width > max_width or image.height > max_height:
                raise ValidationError('Розмір зображення занадто великий. Максимальний розмір: 1100x1100 пікселів.')

            # Проверка веса файла
            max_size = 10 * 1024 * 512  # 10 МБ
            if photo.size > max_size:
                raise ValidationError('Розмір файлу занадто великий. Максимальний розмір: 10 МБ.')

        return photo

class WordComplaintForm(forms.ModelForm):
    class Meta:
        model = WordComplaint
        fields = []


class AvoidedWordForm(forms.ModelForm):
    class Meta:
        model = AvoidedWord
        fields = []
