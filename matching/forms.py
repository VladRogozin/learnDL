from django import forms
from .models import Sentence, AvoidedSentence


class SentenceForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ['text', 'level', 'hide']

    level = forms.ChoiceField(choices=Sentence.LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

class AvoidedSentenceForm(forms.ModelForm):
    class Meta:
        model = AvoidedSentence
        fields = []

