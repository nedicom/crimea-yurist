from django import template
from home.models import ClientReview

register = template.Library()

@register.simple_tag
def get_reviews():
    return ClientReview.objects.filter(is_published=True).order_by('-review_date')

@register.filter
def average_rating(reviews):
    """Рассчитывает средний рейтинг из списка отзывов"""
    if not reviews:
        return 0
    
    total = 0
    count = 0
    
    for review in reviews:
        total += review.rating
        count += 1
    
    if count == 0:
        return 0
    
    return round(total / count, 1)