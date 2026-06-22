from django.core.management.base import BaseCommand
from wagtail.models import Site, Page, Locale
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            locale = Locale.objects.get(language_code=settings.LANGUAGE_CODE)
        except Locale.DoesNotExist:
            locale = Locale(language_code=settings.LANGUAGE_CODE)
            locale.save()
            self.stdout.write("Locale created")

        if not Page.objects.filter(depth=1).exists():
            root = Page.add_root(title="Root")
            self.stdout.write("Root page created")
        else:
            root = Page.get_first_root_node()
            self.stdout.write("Root page exists")

        page_content_type = ContentType.objects.get_for_model(Page)
        
        try:
            home_page = Page.objects.get(slug='home')
            self.stdout.write("Home page exists")
        except Page.DoesNotExist:
            home_page = Page(
                title="Home",
                slug="home",
                content_type=page_content_type,
                locale=locale,
                live=True,
            )
            root.add_child(instance=home_page)
            home_page.save()
            self.stdout.write("Home page created")

        if not Site.objects.exists():
            Site.objects.create(
                hostname='crimea-yurist.ru',
                port=80,
                site_name='Crimea Yurist',
                root_page=home_page,
                is_default_site=True
            )
            self.stdout.write("Site created")
        else:
            self.stdout.write("Site exists")

        # Set page permissions
        from wagtail.models import PagePermissionTester
        from django.contrib.auth.models import User

        try:
            user = User.objects.filter(is_superuser=True).first()
            if user:
                tester = PagePermissionTester(user)
                self.stdout.write(f"User {user.username} can add subpages: {tester.can_add_subpage(home_page)}")
        except Exception as e:
            self.stdout.write(f"Permission check error: {e}")
