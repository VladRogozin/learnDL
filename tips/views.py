from .forms import UserAdviceForm
from django.shortcuts import render, redirect


def add_advice(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = UserAdviceForm(request.POST)
            if form.is_valid():
                advice = form.save(commit=False)
                advice.user = request.user
                advice.save()
                # Можете добавить сообщение об успешной отправке, если нужно
                return render(request, 'base/base.html', {'form': form, 'success_message': 'Спасибо за ваш совет!'})
        else:
            # Пользователь не залогинен, перенаправляем на страницу входа
            return redirect('login')
    else:
        form = UserAdviceForm()
    return render(request, 'base/base.html', {'form': form})
