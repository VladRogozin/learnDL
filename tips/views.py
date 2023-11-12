from .forms import UserAdviceForm
from django.shortcuts import render, redirect

from .models import PageLink


def add_advice(request):
    if request.method == 'POST':
            form = UserAdviceForm(request.POST)
            print(form)
            if form.is_valid():
                advice = form.save(commit=False)
                advice.user = request.user
                advice.save()
                # Можете добавить сообщение об успешной отправке, если нужно
                success_message = 'Спасибо за ваш совет!'
                return render(request, 'base/base.html', {'form': form, 'success_message': success_message})
    else:
        form = UserAdviceForm()

        # Получите связанные объекты PageLink
    page_links = PageLink.objects.all()

    # Создайте список словарей, каждый словарь содержит информацию о странице и ее изображении
    pages_with_icons = []
    for page_link in page_links:
        page = page_link.page
        page_info = {
            'id': page.id,
            'title': page.title,
            'description': page.description,
            'icon_url': page_link.icons.url if page_link.icons else ''  # URL изображения или пустая строка
        }
        pages_with_icons.append(page_info)

    return render(request, 'base/base.html', {'form': form, 'pages_with_icons': pages_with_icons})
