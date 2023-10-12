from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from tips.views import add_advice
from django.contrib.auth import views as auth_views
from accounts.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', add_advice, name='base_view'),
    path('words/', include('base_game.urls')),
    path('my/', include('accounts.urls')),
    path('artikel/', include('artikel.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
