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
    region = models.CharField("Регион", max_length=100, blank=True, default="Республика Крым")
    postal_code = models.CharField("Почтовый индекс", max_length=20, blank=True)
    country = models.CharField("Страна", max_length=100, default="Россия")
    
    phone = models.CharField("Телефон", max_length=20, blank=True)
    email = models.EmailField("Email", blank=True)
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
        ], heading="Герой секция"),
        
        FieldPanel('description'),
        FieldPanel('content'),
        
        MultiFieldPanel([
            FieldPanel('street_address'),
            FieldPanel('city'),
            FieldPanel('region'),
            FieldPanel('postal_code'),
            FieldPanel('country'),
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
                "addressCountry": self.country
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
    region = models.CharField("Регион", max_length=100, blank=True)
    postal_code = models.CharField("Почтовый индекс", max_length=20, blank=True)
    country = models.CharField("Страна", max_length=100, default="Россия")
    
    phone = models.CharField("Телефон", max_length=20, blank=True)
    email = models.EmailField("Email", blank=True)
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
            FieldPanel('country'),
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
                "addressCountry": self.country
            },
            "hasMap": self.map_url if self.map_url else None
        }

    class Meta:
        verbose_name = "Страница города"
        verbose_name_plural = "Страницы городов"


class ServicePage(Page):
    """Страница услуги в городе - Семейный юрист Симферополь"""
    
    # Основная информация об услуге
    service_type = models.CharField("Тип услуги", max_length=200, help_text="Например: Семейный юрист, Недвижимость, Наследство")
    short_description = models.TextField("Краткое описание", max_length=200)
    full_description = RichTextField("Полное описание")
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, null=True, blank=True)
    price_description = models.CharField("Описание цены", max_length=100, blank=True, help_text="Например: от, договорная, бесплатная консультация")
    
    # Адрес оказания услуги (может отличаться от адреса города)
    address = models.TextField("Адрес оказания услуги", blank=True)
    
    # Визуальный контент
    service_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Главное фото услуги"
    )
    
    photos = StreamField([
        ('photo', ImageChooserBlock(verbose_name="Фото")),
    ], use_json_field=True, blank=True, verbose_name="Дополнительные фотографии")
    
    # График работы для этой услуги
    working_hours = StreamField([
        ('day', blocks.StructBlock([
            ('day_name', blocks.ChoiceBlock(choices=[
                ('monday', 'Понедельник'),
                ('tuesday', 'Вторник'),
                ('wednesday', 'Среда'),
                ('thursday', 'Четверг'),
                ('friday', 'Пятница'),
                ('saturday', 'Суббота'),
                ('sunday', 'Воскресенье'),
            ], verbose_name="День недели")),
            ('hours', blocks.CharBlock(verbose_name="Часы работы", help_text="Например: 09:00-18:00")),
        ], verbose_name="Рабочий день"))
    ], use_json_field=True, blank=True, verbose_name="График работы")

    template = "service_page.html"

    # Настройки страницы
    parent_page_types = ['CityPage']  # Можно создавать только в странице города
    subpage_types = []  # Не может иметь дочерних страниц

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('service_type'),
            FieldPanel('service_image'),
        ], heading="Основная информация"),
        
        FieldPanel('short_description'),
        FieldPanel('full_description'),
        
        MultiFieldPanel([
            FieldPanel('price'),
            FieldPanel('price_description'),
        ], heading="Стоимость услуги"),
        
        FieldPanel('address'),
        FieldPanel('photos'),
        FieldPanel('working_hours'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('service_type'),
        index.SearchField('short_description'),
        index.SearchField('full_description'),
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
        
        return {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"{self.service_type} - {city_page.city_name}",
            "description": self.short_description,
            "offeredBy": {
                "@type": "LegalService",
                "name": city_page.city_name
            },
            "areaServed": city_page.city,
            "price": f"{self.price} RUB" if self.price else self.price_description
        }

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"