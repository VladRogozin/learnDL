from django.db import models
from django.contrib.auth.models import User  # Підключення моделі користувача Django

from accounts.models import Pages


class UserAdvice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Зв'язок з користувачем Django
    message = models.TextField()  # Текстове поле для повідомлення
    timestamp = models.DateTimeField(auto_now_add=True)  # Дата та час створення повідомлення

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"


class PageLink(models.Model):
    page = models.ForeignKey(Pages, on_delete=models.CASCADE)
    icons = models.ImageField(upload_to='user_icons/', blank=True, null=True)

    def get_page_display(self):
        return self.page.title

    get_page_display.short_description = 'Page Title'
