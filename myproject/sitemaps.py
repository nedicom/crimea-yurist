from django.contrib.sitemaps import Sitemap
from wagtail.models import Page, Site as WagtailSite
from django.conf import settings

class FixedSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def _get_domain(self):
        """Получаем домен только из Wagtail или ALLOWED_HOSTS"""
        # 1. Пробуем получить из Wagtail Site
        wagtail_site = WagtailSite.find_for_request(None)
        if wagtail_site:
            print(f"Using Wagtail site: {wagtail_site.hostname}")
            return wagtail_site.hostname
        
        # 2. Используем ALLOWED_HOSTS
        if hasattr(settings, 'ALLOWED_HOSTS') and settings.ALLOWED_HOSTS:
            # Берем первый не-wildcard хост
            for host in settings.ALLOWED_HOSTS:
                if host != '*' and not host.startswith('.'):
                    print(f"Using ALLOWED_HOSTS: {host}")
                    return host
        
        # 3. Fallback на настройку или дефолтный домен
        fallback_domain = getattr(settings, 'SITE_DOMAIN', 'crimea-yurist.ru')
        print(f"Using fallback: {fallback_domain}")
        return fallback_domain

    def items(self):
        return Page.objects.live().public().exclude(depth=1).exclude(slug='root')

    def location(self, item):
        if item.depth == 2:
            return "/"
        else:
            return f"/{item.slug}/"

    def get_urls(self, page=1, site=None, protocol=None):
        urls = []
        domain = self._get_domain()
        
        print(f"Final domain for sitemap: {domain}")
        
        for item in self.paginator.page(page).object_list:
            if item.depth == 2:
                path = ""
            else:
                path = item.slug
            
            if settings.DEBUG:
                loc = f"http://127.0.0.1:8000/{path}" if path else "http://127.0.0.1:8000/"
            else:
                # Очищаем домен от порта для production
                domain_clean = domain.split(':')[0]
                loc = f"https://{domain_clean}/{path}" if path else f"https://{domain_clean}/"
            
            url_info = {
                'item': item,
                'location': loc,
                'lastmod': self.lastmod(item),
                'changefreq': self.changefreq,
                'priority': self._get_priority(item),
            }
            urls.append(url_info)
        
        return urls

    def _get_priority(self, item):
        if item.depth <= 3:
            return 1.0
        elif item.depth <= 4:
            return 0.8
        else:
            return 0.6

    def lastmod(self, item):
        return item.last_published_at