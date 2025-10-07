from django.db import models
from wagtail.models import Page
from wagtail import blocks
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.images.models import Image


class HomePage(Page):
    """Главная страница сайта - Юрист по Крыму"""
    hero_title = models.CharField("Заголовок", max_length=255, blank=True, default="Юрист по Крыму")
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фон картинки"
    )
    
    # Контактная информация для главной страницы
    street_address = models.CharField("Улица, дом", max_length=255, blank=True)
    city = models.CharField("Город", max_length=100, blank=True, default="Симферополь")
    region = models.CharField("Регион", max_length=100, default="Республика Крым")
    postal_code = models.CharField("Почтовый индекс", max_length=20, blank=True)
    
    phone = models.CharField("Телефон", max_length=20, default="+7 978 910-42-97")
    email = models.EmailField("Email", default="mail@crimea-yurist.ru")
    map_url = models.URLField("Ссылка на карту", blank=True)
    
    description = RichTextField("Описание услуг", blank=True)
    
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon="title", verbose_name="Заголовок")),
        ('paragraph', blocks.RichTextBlock(icon="pilcrow", verbose_name="Текст")),
        ('image', ImageChooserBlock(icon="image", verbose_name="Картинка")),
    ], use_json_field=True, blank=True, verbose_name="Контент")

    template = "home_page.html"

    # Настройки страницы
    parent_page_types = []  # Только в корне сайта
    subpage_types = ['CityPage']  # Можно создавать только страницы городов
    max_count = 1  # Только одна главная страница

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_image'),
        ], heading="Герой Фото юриста"),
        
        FieldPanel('description'),
        FieldPanel('content'),
        
        MultiFieldPanel([
            FieldPanel('street_address'),
            FieldPanel('city'),
            FieldPanel('region'),
            FieldPanel('postal_code'),
            FieldPanel('map_url'),
        ], heading="Адрес и география"),
        
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
        ], heading="Контактная информация"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('hero_title'),
        index.SearchField('description'),
        index.SearchField('content'),
        index.SearchField('street_address'),
        index.SearchField('city'),
        index.SearchField('region'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Добавляем все города в контекст главной страницы
        context['cities'] = CityPage.objects.live().public()
        return context

    def get_schema_org_data(self):
        """Генерация данных для Schema.org для главной страницы"""
        return {
            "@context": "https://schema.org",
            "@type": "LegalService",
            "name": self.hero_title or self.title,
            "description": self.description,
            "telephone": self.phone,
            "email": self.email,
            "url": self.full_url,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": self.street_address,
                "addressLocality": self.city,
                "addressRegion": self.region,
                "postalCode": self.postal_code,
            },
            "hasMap": self.map_url if self.map_url else None
        }

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главные страницы"


class CityPage(Page):
    """Страница города - Юрист Симферополь"""
    city_name = models.CharField("Название города", max_length=100, help_text="Например: Юрист Симферополь")
    
    # Герой секция для города
    hero_title = models.CharField("Заголовок", max_length=255, blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фон картинки"
    )
    
    # Адрес и контакты
    street_address = models.CharField("Улица, дом", max_length=255, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    region = models.CharField("Регион", max_length=100, default="Республика Крым")
    postal_code = models.CharField("Почтовый индекс", max_length=20, blank=True)
    
    phone = models.CharField("Телефон", max_length=20,  default="+7 978 910-42-97")
    email = models.EmailField("Email", default="mail@crimea-yurist.ru")
    map_url = models.URLField("Ссылка на карту", blank=True)
    
    # Описание и контент
    description = RichTextField("Описание услуг в городе", blank=True)
    
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon="title", verbose_name="Заголовок")),
        ('paragraph', blocks.RichTextBlock(icon="pilcrow", verbose_name="Текст")),
        ('image', ImageChooserBlock(icon="image", verbose_name="Картинка")),
    ], use_json_field=True, blank=True, verbose_name="Дополнительный контент")

    template = "city_page.html"

    # Настройки страницы
    parent_page_types = ['HomePage']  # Можно создавать только в главной
    subpage_types = ['ServicePage']  # Можно создавать страницы услуг

    content_panels = Page.content_panels + [
        FieldPanel('city_name'),
        
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_image'),
        ], heading="Герой секция"),
        
        FieldPanel('description'),
        FieldPanel('content'),
        
        MultiFieldPanel([
            FieldPanel('street_address'),
            FieldPanel('city'),
            FieldPanel('region'),
            FieldPanel('postal_code'),
            FieldPanel('map_url'),
        ], heading="Адрес и география"),
        
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
        ], heading="Контактная информация"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('city_name'),
        index.SearchField('description'),
        index.SearchField('content'),
        index.SearchField('street_address'),
        index.SearchField('city'),
        index.SearchField('region'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Добавляем услуги этого города в контекст
        context['services'] = ServicePage.objects.child_of(self).live()
        return context

    def get_schema_org_data(self):
        """Генерация данных для Schema.org"""
        return {
            "@context": "https://schema.org",
            "@type": "LegalService",
            "name": self.city_name or self.title,
            "description": self.description,
            "telephone": self.phone,
            "email": self.email,
            "url": self.full_url,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": self.street_address,
                "addressLocality": self.city,
                "addressRegion": self.region,
                "postalCode": self.postal_code,
            },
            "hasMap": self.map_url if self.map_url else None
        }

    class Meta:
        verbose_name = "Страница города"
        verbose_name_plural = "Страницы городов"


class ServicePage(Page):
    """Страница услуги - Семейный юрист Симферополь"""
    
    # Герой секция для услуги
    hero_title = models.CharField("Заголовок", max_length=255, blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фон картинки"
    )
    
    # Основная информация
    service_type = models.CharField("Тип услуги", max_length=200, help_text="Например: Семейный юрист, Недвижимость, Наследство")
    short_description = models.TextField("Краткое описание", max_length=200)
    
    # Стоимость услуги
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, null=True, blank=True, default=1000)
    price_description = models.CharField("Описание цены", max_length=100, blank=True, default="от", help_text="Например: от, договорная, бесплатная консультация")
    
    # Адрес оказания услуги (может отличаться от адреса города)
    street_address = models.CharField("Улица, дом", max_length=255, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    region = models.CharField("Регион", max_length=100, default="Республика Крым")
    postal_code = models.CharField("Почтовый индекс", max_length=20, blank=True)
    
    # Контакты для услуги
    phone = models.CharField("Телефон", max_length=20, default="+7 978 910-42-97")
    email = models.EmailField("Email", default="mail@crimea-yurist.ru")
    map_url = models.URLField("Ссылка на карту", blank=True)
    
    # Описание и контент
    description = RichTextField("Описание услуги", blank=True)
    
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon="title", verbose_name="Заголовок")),
        ('paragraph', blocks.RichTextBlock(icon="pilcrow", verbose_name="Текст")),
        ('image', ImageChooserBlock(icon="image", verbose_name="Картинка")),
    ], use_json_field=True, blank=True, verbose_name="Дополнительный контент")

    template = "service_page.html"

    # Настройки страницы
    parent_page_types = ['CityPage']  # Можно создавать только в странице города
    subpage_types = []  # Не может иметь дочерних страниц

    content_panels = Page.content_panels + [        
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_image'),
        ], heading="Герой секция"),
        
        MultiFieldPanel([
            FieldPanel('service_type'),
            FieldPanel('short_description'),
        ], heading="Основная информация"),
        
        FieldPanel('description'),
        FieldPanel('content'),
        
        MultiFieldPanel([
            FieldPanel('price'),
            FieldPanel('price_description'),
        ], heading="Стоимость услуги"),
        
        MultiFieldPanel([
            FieldPanel('street_address'),
            FieldPanel('city'),
            FieldPanel('region'),
            FieldPanel('postal_code'),
            FieldPanel('map_url'),
        ], heading="Адрес оказания услуги"),
        
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
        ], heading="Контактная информация для услуги"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('service_name'),
        index.SearchField('service_type'),
        index.SearchField('short_description'),
        index.SearchField('description'),
        index.SearchField('content'),
        index.FilterField('price'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Добавляем родительский город в контекст
        context['city'] = self.get_parent().specific
        return context

    def get_schema_org_data(self):
        """Генерация данных для Schema.org для услуги"""
        city_page = self.get_parent().specific
        
        schema_data = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": self.service_name or self.title,
            "description": self.short_description or self.description,
            "serviceType": self.service_type,
        }
        
        # Добавляем цену, если указана
        if self.price:
            schema_data["offers"] = {
                "@type": "Offer",
                "price": str(self.price),
                "priceCurrency": "RUB",
                "description": self.price_description
            }
        elif self.price_description:
            schema_data["offers"] = {
                "@type": "Offer",
                "priceSpecification": {
                    "@type": "PriceSpecification",
                    "description": self.price_description
                }
            }
        
        # Добавляем адрес, если указан
        if any([self.street_address, self.city, self.region]):
            schema_data["areaServed"] = {
                "@type": "Place",
                "name": f"{self.city}, {self.region}" if self.city and self.region else self.city or self.region
            }
            
            if any([self.street_address, self.city, self.region, self.postal_code]):
                schema_data["areaServed"]["address"] = {
                    "@type": "PostalAddress",
                    "streetAddress": self.street_address,
                    "addressLocality": self.city,
                    "addressRegion": self.region,
                    "postalCode": self.postal_code,
                }
        
        # Добавляем контакты
        if self.phone:
            schema_data["telephone"] = self.phone
        if self.email:
            schema_data["email"] = self.email
        
        # Добавляем ссылку на карту
        if self.map_url:
            schema_data["hasMap"] = self.map_url
        
        # Добавляем информацию о провайдере услуги (город)
        schema_data["provider"] = {
            "@type": "LegalService",
            "name": city_page.city_name,
            "url": city_page.full_url
        }
        
        return schema_data

    class Meta:
        verbose_name = "Страница услуги"
        verbose_name_plural = "Страницы услуг"