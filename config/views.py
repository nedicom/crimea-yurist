from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegisterForm

def home_page(request):
    context = {
        'title': 'Крымский Юрист - Юридические услуги в Крыму',
        'services': [
            'Юридические консультации',
            'Составление документов',
            'Представительство в суде',
            'Недвижимость и сделки',
            'Банкротство физических лиц'
        ],
        'phone': '+7 (978) 123-45-67',
        'email': 'info@crimea-yurist.ru'
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')  # Замените 'home' на имя вашего URL
    else:
        form = UserRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})