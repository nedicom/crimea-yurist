from django.db import models
from wagtail.models import Page
from wagtail import blocks
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


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
    map_url = models.URLField("Ссылка на карту", blank=True, default="https://yandex.ru/map-widget/v1/?ll=34.097897%2C44.954033&mode=search&oid=245071578035&ol=biz&z=16.64")
    
    description = RichTextField("Описание услуг", blank=True)
    
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon="title", verbose_name="Заголовок")),
        ('paragraph', blocks.RichTextBlock(icon="pilcrow", verbose_name="Текст")),
        ('image', ImageChooserBlock(icon="image", verbose_name="Картинка")),
    ], use_json_field=True, blank=True, verbose_name="Контент")

    template = "home_page.html"

    # Настройки страницы
    parent_page_types = []  # Только в корне сайта
    subpage_types = ['CityPage', 'home.HomePage', 'wagtailcore.Page'] # Можно создавать только страницы городов
    max_count = 1  # Только одна главная страница

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_image'),
        ], heading="Фото услуги"),
        
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
    city_name = models.CharField("Название услуги по городу", max_length=100, help_text="Например: Юрист Симферополь")
    
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
    map_url = models.URLField("Ссылка на карту", blank=True, default="https://yandex.ru/map-widget/v1/?ll=34.097897%2C44.954033&mode=search&oid=245071578035&ol=biz&z=16.64")
    
    # Описание и контент
    description = RichTextField("УТП описание услуг в городе", blank=True)
    
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon="title", verbose_name="Заголовок")),
        ('paragraph', blocks.RichTextBlock(icon="pilcrow", verbose_name="Текст")),
        ('image', ImageChooserBlock(icon="image", verbose_name="Картинка")),
    ], use_json_field=True, blank=True, verbose_name="Подробное описание")

    template = "city_page.html"

    # Настройки страницы
    parent_page_types = ['HomePage']  # Можно создавать только в главной
    subpage_types = ['ServicePage']  # Можно создавать страницы услуг

    content_panels = Page.content_panels + [
        FieldPanel('city_name'),
        
        MultiFieldPanel([
            FieldPanel('hero_image'),
        ], heading="Фото услуги"),
        
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
        related_name='+'
    )
    
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
    map_url = models.URLField("Ссылка на карту", blank=True, default="https://yandex.ru/map-widget/v1/?ll=34.097897%2C44.954033&mode=search&oid=245071578035&ol=biz&z=16.64")
    
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
            FieldPanel('hero_image'),
        ], heading="Фото услуги"),
        
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
            "name": self.title,
            "description": self.description,
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
        
        
class PracticeGalleryPage(Page):
    """Страница-галерея юридической практики"""
    
    description = RichTextField("Описание галереи", blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]
    
    subpage_types = ['LegalPracticePage']
    template = "practice_gallery_page.html"
    
    class Meta:
        verbose_name = "Галерея практики"
        verbose_name_plural = "Галереи практики"


class LegalPracticePage(Page):
    """Страница юридической практики (кейса)"""
    
    # Основная информация о деле
    case_title = models.CharField("Название дела", max_length=255)
    case_type = models.CharField("Тип дела", max_length=100, blank=True, 
                                help_text="Например: Гражданское дело, Уголовное дело и т.д.")
    
    # Детали дела
    case_description = RichTextField("Описание дела", blank=True)
    challenge = RichTextField("Проблема/Задача", blank=True, help_text="С какой проблемой обратился клиент")
    solution = RichTextField("Решение/Результат", blank=True, help_text="Как была решена проблема")
    
    # Даты
    start_date = models.DateField("Дата начала дела", null=True, blank=True)
    end_date = models.DateField("Дата завершения дела", null=True, blank=True)
    
    # Статус дела
    status = models.CharField("Статус дела", max_length=100, blank=True,
                             help_text="Например: Выиграно, Урегулировано, В процессе и т.д.")
    
    # Суд/орган рассмотрения
    court = models.CharField("Суд/Орган", max_length=255, blank=True)
    
    # Галерея изображений
    gallery_images = StreamField([
        ('image', ImageChooserBlock(icon="image", verbose_name="Изображение")),
    ], use_json_field=True, blank=True, verbose_name="Галерея изображений")

    content_panels = Page.content_panels + [
        FieldPanel('case_title'),
        FieldPanel('case_type'),
        FieldPanel('case_description'),
        
        MultiFieldPanel([
            FieldPanel('start_date'),
            FieldPanel('end_date'),
            FieldPanel('status'),
            FieldPanel('court'),
        ], heading="Детали дела"),
        
        FieldPanel('challenge'),
        FieldPanel('solution'),
        FieldPanel('gallery_images'),
        
        InlinePanel('client_reviews', label="Отзывы клиентов"),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('case_title'),
        index.SearchField('case_description'),
        index.SearchField('challenge'),
        index.SearchField('solution'),
        index.SearchField('case_type'),
        index.SearchField('status'),
    ]
    
    parent_page_types = ['PracticeGalleryPage']
    subpage_types = []
    
    template = "legal_practice_page.html"
    
    def get_context(self, request):
        context = super().get_context(request)
        context['reviews'] = self.client_reviews.all()
        return context
    
    class Meta:
        verbose_name = "Юридическая практика"
        verbose_name_plural = "Юридическая практика"


class ClientReview(ClusterableModel):
    """Отзыв клиента о юридической услуге"""
    
    page = ParentalKey(
        LegalPracticePage,
        on_delete=models.CASCADE,
        related_name='client_reviews',
        verbose_name="Страница практики"
    )
    
    # Информация о клиенте
    client_name = models.CharField("ФИО клиента", max_length=255)
    client_initials = models.CharField("Инициалы", max_length=10, blank=True)
    
    # Отзыв
    review_title = models.CharField("Заголовок отзыва", max_length=255)
    review_text = RichTextField("Текст отзыва")
    
    # Оценка
    RATING_CHOICES = [
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    ]
    rating = models.IntegerField("Оценка", choices=RATING_CHOICES, default=5)
    
    # Тип дела для отзыва
    case_type_review = models.CharField("Тип дела", max_length=100, blank=True)
    
    # Публикация
    is_published = models.BooleanField("Опубликован", default=True)
    
    # Дата отзыва
    review_date = models.DateField("Дата отзыва", auto_now_add=True)

    panels = [
        FieldPanel('client_name'),
        FieldPanel('client_initials'),
        FieldPanel('review_title'),
        FieldPanel('review_text'),
        FieldPanel('rating'),
        FieldPanel('case_type_review'),
        FieldPanel('is_published'),
    ]
    
    def __str__(self):
        return f"{self.client_name} - {self.rating}⭐"
    
    class Meta:
        verbose_name = "Отзыв клиента"
        verbose_name_plural = "Отзывы клиентов"
        ordering = ['-review_date']