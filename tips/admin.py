from django.contrib import admin
from .models import UserAdvice


@admin.register(UserAdvice)
class WordComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')
