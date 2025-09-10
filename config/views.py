from django.shortcuts import render

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