from django import forms
from .models import BaseGameModel, WordComplaint
from .models import AvoidedWord



class BaseGameForms(forms.ModelForm):
    class Meta:
        model = BaseGameModel
        fields = ['word', 'description', 'translate', 'autor', 'level', 'hide']

    level = forms.ChoiceField(choices=BaseGameModel.LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


class WordComplaintForm(forms.ModelForm):
    class Meta:
        model = WordComplaint
        fields = []


class AvoidedWordForm(forms.ModelForm):
    class Meta:
        model = AvoidedWord
        fields = []
