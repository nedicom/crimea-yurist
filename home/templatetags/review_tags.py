from django import template
from home.models import ClientReview  # замените 'home' на ваше приложение

register = template.Library()

@register.simple_tag
def get_reviews():
    return ClientReview.objects.filter(is_published=True).order_by('-review_date')