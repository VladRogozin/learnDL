from django import forms
from .models import Sentence, AvoidedSentence
from django.core.exceptions import ValidationError
from PIL import Image


class SentenceForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ['text', 'translate', 'helpText', 'level', 'hide', 'photo']

    level = forms.ChoiceField(choices=Sentence.LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')

        if not text:
            self.add_error('text', 'Це поле обов\'язкове для заповнення.')

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


class AvoidedSentenceForm(forms.ModelForm):
    class Meta:
        model = AvoidedSentence
        fields = []

