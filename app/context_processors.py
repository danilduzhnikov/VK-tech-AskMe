from .models import Tag

def popular_tags(request):
    return {
        'popular_tags': Tag.objects.get_popular(),
    }