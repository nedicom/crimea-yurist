from django.db import models
from wagtail.models import Page
from wagtail import blocks
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock

class HomePage(Page):
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon="title", verbose_name="Заголовок")),
        ('paragraph', blocks.RichTextBlock(icon="pilcrow", verbose_name="Текст")),
        ('image', ImageChooserBlock(icon="image", verbose_name="Картинка")),
    ], use_json_field=True, blank=True)

    template = "home_page.html"

    # ВАЖНО: ограничения для HomePage
    parent_page_types = []  # HomePage можно создавать только в корне
    subpage_types = ['BlogPage']  # В HomePage можно создавать только BlogPage
    max_count = 1  # Только одна домашняя страница

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]

class BlogPage(Page):
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon="title", verbose_name="Заголовок")),
        ('paragraph', blocks.RichTextBlock(icon="pilcrow", verbose_name="Текст")),
        ('image', ImageChooserBlock(icon="image", verbose_name="Картинка")),
    ], use_json_field=True, blank=True)

    template = "blog_page.html"
    
    # ВАЖНО: ограничения для BlogPage
    parent_page_types = ['HomePage']  # BlogPage можно создавать только в HomePage
    subpage_types = []  # BlogPage не может иметь дочерних страниц

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]

    class Meta:
        verbose_name = "Blog Page"
        verbose_name_plural = "Blog Pages"