from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import QuestionTag, Tag, Question

from collections import defaultdict
from django.db.models.query import QuerySet

# Стартовые свойства пагинатора
def paginators_params(request, content, count):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(content, count)

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page, paginator

# кастыльная пагинация
def paginations_params(request, content, count):
    page, paginator = paginators_params(request, content, count)

    two_pages_ahead = page.number + 2
    two_pages_behind = page.number - 2
    try:
        arrows_left_border = paginator.page(two_pages_behind)
        left_switch = True
    except:
        left_switch = False
        arrows_left_border = None
    try:
        arrows_right_border = paginator.page(two_pages_ahead)
        right_switch = True
    except:
        right_switch = False
        arrows_right_border = None

    is_first_page = True if page.number == 1 else False
    is_last_page = True if page.number == paginator.num_pages else False

    params = {
        'page_obj': page,
        'paginator': paginator,
        'left_switch': left_switch,
        'right_switch': right_switch,
        'is_first_page': is_first_page,
        'is_last_page': is_last_page,
        'arrows_left_border': arrows_left_border,
        'arrows_right_border': arrows_right_border,
        'two_pages_ahead': two_pages_ahead,
        'two_pages_behind': two_pages_behind
    }

    return {
        'page_objects': page.object_list,
        'params': params,
        'paginator': paginator
    }

def questions_list_tags(questions):
    question_tags = []
    # questions несколько
    try:
        for question in questions:
            # Получаем все записи QuestionTag, где question_id совпадает с переданным значением
            question_tag_records = QuestionTag.objects.filter(question_id=question.id)

            # Извлекаем уникальные теги из этих записей
            tags = Tag.objects.filter(id__in=[record.tag_id for record in question_tag_records])

            question_tags.append(
                {
                    'question': question,
                    'tags': tags
                }
            )
    # questions один
    except:
        # Получаем все записи QuestionTag, где question_id совпадает с переданным значением
        question_tag_records = QuestionTag.objects.filter(question_id=questions.id)

        # Извлекаем уникальные теги из этих записей
        tags = Tag.objects.filter(id__in=[record.tag_id for record in question_tag_records])
        question_tags.append(
            {
                'question': questions,
                'tags': tags
            }
        )
    return question_tags