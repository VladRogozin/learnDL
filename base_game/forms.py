from django import forms
from .models import BaseGameModel, WordComplaint


class BaseGameForms(forms.ModelForm):
    class Meta:
        model = BaseGameModel
        fields = ['word', 'description', 'translate', 'autor', 'level']

    level = forms.ChoiceField(choices=BaseGameModel.LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


class WordComplaintForm(forms.ModelForm):
    class Meta:
        model = WordComplaint
        fields = []
