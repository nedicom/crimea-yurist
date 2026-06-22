# myproject/views.py
from django.shortcuts import render

def custom_404(request, exception=None):
    """Кастомная страница 404"""
    return render(request, '404.html', status=404)

def custom_500(request):
    """Кастомная страница 500"""
    return render(request, '500.html', status=500)


def sitemap_html(request):
    """Человеческая карта сайта /karta-sayta/ — города, услуги и разделы."""
    from wagtail.models import Page
    from home.models import HomePage, CityPage, ServicePage

    home = HomePage.objects.live().first()

    cities = []
    for city in CityPage.objects.live().public().order_by('title'):
        cities.append({
            'city': city,
            'services': ServicePage.objects.child_of(city).live().public().order_by('title'),
        })

    city_ids = list(CityPage.objects.values_list('id', flat=True))
    other_sections = (
        Page.objects.live().public().filter(depth=3)
        .exclude(id__in=city_ids)
        .order_by('title')
    )

    return render(request, 'sitemap_html.html', {
        'home': home,
        'cities': cities,
        'other_sections': other_sections,
    })