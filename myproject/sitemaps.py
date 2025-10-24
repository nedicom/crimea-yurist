from wagtail.contrib.sitemaps import Sitemap
from wagtail.models import Page

class CustomSitemap(Sitemap):
    def items(self):
        return Page.objects.live().public()
    
    def location(self, item):
        return item.get_full_url(request=None)
    
    def get_urls(self, page=1, site=None, protocol=None):
        # Получаем все URL
        urls = super().get_urls(page, site, protocol)
        
        filtered_urls = []
        for url in urls:
            # Фильтруем только те, где location не None и не пустой
            if url['location'] and url['location'] != 'None':
                # Заменяем http:// на https://
                url['location'] = url['location'].replace('http://', 'https://')
                filtered_urls.append(url)
        
        return filtered_urls