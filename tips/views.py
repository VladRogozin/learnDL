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

    # Получите связанные объекты Pages через PageLink
    page_links = PageLink.objects.all()
    pages = [page_link.page for page_link in page_links]

    return render(request, 'base/base.html', {'form': form, 'pages': pages})
