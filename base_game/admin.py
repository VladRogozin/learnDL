from django.contrib import admin
from .models import BaseGameModel
from .models import WordComplaint


@admin.register(WordComplaint)
class WordComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'timestamp')


class BaseGameModelAdmin(admin.ModelAdmin):
    list_display = ('word', 'description', 'translate', 'autor', 'level')
    list_filter = ('level', )


admin.site.register(BaseGameModel, BaseGameModelAdmin)
