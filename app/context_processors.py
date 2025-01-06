from django.db.models import Count
from .models import Tag, AnswerLike, CustomUser


def popular_persons(request):
    popular_persons = AnswerLike.objects.values('user') \
                    .annotate(likes_count=Count('user')) \
                    .order_by('-likes_count')[:5]

    popular_persons = [user['user'] for user in popular_persons]


    popular_persons = CustomUser.objects.filter(id__in=popular_persons)

    return {
        'popular_persons': popular_persons
    }

def popular_tags(request):
    return {
        'popular_tags': Tag.objects.get_popular(),
    }