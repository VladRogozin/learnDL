from django import forms
from .models import UserAdvice


class UserAdviceForm(forms.ModelForm):
    class Meta:
        model = UserAdvice
        fields = ['message']

