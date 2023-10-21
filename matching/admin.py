from django.contrib import admin
from .models import Sentence


class SentenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')  # Replace 'id' and 'text' with the actual fields you want to display


admin.site.register(Sentence, SentenceAdmin)
