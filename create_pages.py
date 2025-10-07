from django.core.management.base import BaseCommand
from wagtail.models import Site, Page
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Page.objects.filter(depth=1).exists():
            root = Page.add_root(title="Root")
            self.stdout.write("Корневая страница создана")
        else:
            root = Page.get_first_root_node()
            self.stdout.write("Корневая страница уже существует")

        page_content_type = ContentType.objects.get_for_model(Page)
        
        try:
            home_page = Page.objects.get(slug='home')
            self.stdout.write("Домашняя страница уже существует")
        except Page.DoesNotExist:
            home_page = Page(
                title="Home",
                slug="home",
                content_type=page_content_type,
                live=True,
            )
            root.add_child(instance=home_page)
            self.stdout.write("Домашняя страница создана")

        if not Site.objects.exists():
            Site.objects.create(
                hostname='crimea-yurist.ru',
                port=80,
                site_name='Crimea Yurist',
                root_page=home_page,
                is_default_site=True
            )
            self.stdout.write("Сайт создан")
        else:
            self.stdout.write("Сайт уже существует")