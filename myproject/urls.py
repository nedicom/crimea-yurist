from django.conf import settings
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps import Sitemap

from search import views as search_views
from .sitemaps import CustomSitemap
from .views import custom_404, custom_500

wagtail_sitemap = Sitemap()

sitemaps = {
    'pages': CustomSitemap(),
}

handler404 = custom_404
handler500 = custom_500

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),

    # sitemap.xml
    path('sitemap.xml', sitemap, {'sitemaps': {'pages': CustomSitemap}}),

    # Robots.txt
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain'
    )),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
        path("", include(wagtail_urls)),
    ]