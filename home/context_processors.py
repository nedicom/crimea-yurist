from wagtail.models import Page

def menu_pages(request):
    return {
        'menu_pages': Page.objects.live().public().in_menu()
    }