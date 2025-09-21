from django.db import models

from wagtail.models import Page
from wagtail import blocks
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel
# Правильный импорт для ImageChooserBlock
from wagtail.images.blocks import ImageChooserBlock

class HomePage(Page):
    # Поле StreamField состоит из набора блоков
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", icon="title", verbose_name="Заголовок")),
        ('paragraph', blocks.RichTextBlock(icon="pilcrow", verbose_name="Текст")),
        # Теперь ImageChooserBlock импортирован правильно
        ('image', ImageChooserBlock(icon="image", verbose_name="Картинка")),
    ], use_json_field=True, blank=True)

    template = "home_page.html"

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]