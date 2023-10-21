from django import forms

from .models import AvoidedArticle


class AvoidedArticleForm(forms.ModelForm):
    class Meta:
        model = AvoidedArticle
        fields = []