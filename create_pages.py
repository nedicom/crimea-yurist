import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from wagtail.models import Site, Page
from django.contrib.contenttypes.models import ContentType

def create_pages():
    if not Page.objects.filter(depth=1).exists():
        root = Page.add_root(title="Root")
        print("Корневая страница создана")
    else:
        root = Page.get_first_root_node()
        print("Корневая страница уже существует")

    page_content_type = ContentType.objects.get_for_model(Page)
    
    try:
        home_page = Page.objects.get(slug='home')
        print("Домашняя страница уже существует")
    except Page.DoesNotExist:
        home_page = Page(
            title="Home",
            slug="home",
            content_type=page_content_type,
            live=True,
        )
        root.add_child(instance=home_page)
        print("Домашняя страница создана")

    if not Site.objects.exists():
        Site.objects.create(
            hostname='crimea-yurist.ru',
            port=80,
            site_name='Crimea Yurist',
            root_page=home_page,
            is_default_site=True
        )
        print("Сайт создан")
    else:
        print("Сайт уже существует")

if __name__ == '__main__':
    create_pages()