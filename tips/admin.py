from django.contrib import admin
from .models import UserAdvice, PageLink


@admin.register(UserAdvice)
class UserAdviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')


@admin.register(PageLink)
class PageLinkAdmin(admin.ModelAdmin):
    list_display = ('get_page_display',)

    def get_page_title(self, obj):
        return obj.page.title
    get_page_title.short_description = 'Page Title'
