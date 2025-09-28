# home/templatetags/custom_menu.py
from django import template
from wagtail.models import Page

register = template.Library()

@register.inclusion_tag('tags/custom_menu.html', takes_context=True)
def show_nested_menu(context, show_children=True):
    parent_pages = Page.objects.filter(depth=3).live().public().in_menu()
    
    # Добавляем дочерние страницы для каждого родителя
    pages_with_children = []
    for parent in parent_pages:
        pages_with_children.append({
            'parent': parent,
            'children': parent.get_children().live().public().in_menu() if show_children else None
        })
    
    return {
        'pages_with_children': pages_with_children,
        'request': context['request']
    }