from django.db import models
from wagtail.models import Page
from wagtail import blocks
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

class HomePage(Page):
    """Главная страница сайта"""
    hero_title = models.CharField("Заголовок героя", max_length=255, blank=True)
    hero_subtitle = models.TextField("Подзаголовок героя", blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Фон героя"
    )
    
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon="title", verbose_name="Заголовок")),
        ('paragraph', blocks.RichTextBlock(icon="pilcrow", verbose_name="Текст")),
        ('image', ImageChooserBlock(icon="image", verbose_name="Картинка")),
        ('cities_gallery', blocks.ListBlock(
            blocks.PageChooserBlock(page_type='city.CityPage'),
            icon='group',
            verbose_name='Галерея городов'
        )),
    ], use_json_field=True, blank=True, verbose_name="Контент")

    template = "home_page.html"

    # Настройки страницы
    parent_page_types = []  # Только в корне сайта
    subpage_types = ['CityPage']  # Можно создавать только страницы городов
    max_count = 1  # Только одна главная страница

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_image'),
        ], heading="Герой секция"),
        FieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('hero_title'),
        index.SearchField('content'),
    ]

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главные страницы"

class CityPage(Page):
    """Страница города"""
    city_name = models.CharField("Название города", max_length=100)
    population = models.PositiveIntegerField("Население", null=True, blank=True)
    description = RichTextField("Описание города", blank=True)
    main_photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Главное фото"
    )
    map_url = models.URLField("Ссылка на карту", blank=True)
    
    contact_info = StreamField([
        ('phone', blocks.CharBlock(verbose_name="Телефон")),
        ('email', blocks.EmailBlock(verbose_name="Email")),
        ('address', blocks.TextBlock(verbose_name="Адрес")),
    ], use_json_field=True, blank=True, verbose_name="Контактная информация")

    template = "city_page.html"

    # Настройки страницы
    parent_page_types = ['HomePage']  # Можно создавать только в главной
    subpage_types = ['ServicePage']  # Можно создавать страницы услуг

    content_panels = Page.content_panels + [
        FieldPanel('city_name'),
        FieldPanel('population'),
        FieldPanel('description'),
        FieldPanel('main_photo'),
        FieldPanel('map_url'),
        FieldPanel('contact_info'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('city_name'),
        index.SearchField('description'),
        index.FilterField('population'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Добавляем услуги этого города в контекст
        context['services'] = ServicePage.objects.child_of(self).live()
        return context

    class Meta:
        verbose_name = "Страница города"
        verbose_name_plural = "Страницы городов"

class ServicePage(Page):
    """Страница услуги в городе"""    
    short_description = models.TextField("Краткое описание", max_length=200)
    full_description = RichTextField("Полное описание")
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, null=True, blank=True)
    address = models.TextField("Адрес оказания услуги")
    
    photos = StreamField([
        ('photo', ImageChooserBlock(verbose_name="Фото")),
    ], use_json_field=True, blank=True, verbose_name="Фотографии")
    
    working_hours = StreamField([
        ('day', blocks.StructBlock([
            ('day_name', blocks.CharBlock(verbose_name="День недели")),
            ('hours', blocks.CharBlock(verbose_name="Часы работы")),
        ], verbose_name="Рабочий день"))
    ], use_json_field=True, blank=True, verbose_name="График работы")

    template = "service_page.html"

    # Настройки страницы
    parent_page_types = ['CityPage']  # Можно создавать только в странице города
    subpage_types = []  # Не может иметь дочерних страниц

    content_panels = Page.content_panels + [
        FieldPanel('short_description'),
        FieldPanel('full_description'),
        FieldPanel('price'),
        FieldPanel('address'),
        FieldPanel('photos'),
        FieldPanel('working_hours'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('short_description'),
        index.SearchField('full_description'),
        index.FilterField('price'),
    ]

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"