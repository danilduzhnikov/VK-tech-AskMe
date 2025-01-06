from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import QuestionTag, Tag

# Стартовые свойства пагинатора
def paginators_params(request, content, count):
    """
    Функция возвращает объект текущей страницы и пагинатор.
    """
    page_num = request.GET.get('page', 1)
    paginator = Paginator(content, count)

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page, paginator


def paginations_params(request, content, count):
    """
    Расширенная пагинация, включающая переключатели страниц и дополнительные параметры.
    Поддерживает все случаи: пустой контент, большие объемы данных и разные параметры.
    """
    # Проверка, если content пустой
    if not content:
        return {
            'page_objects': [],
            'params': {
                'page_obj': None,
                'paginator': None,
                'left_switch': False,
                'right_switch': False,
                'is_first_page': True,
                'is_last_page': True,
                'arrows_left_border': None,
                'arrows_right_border': None,
                'two_pages_ahead': None,
                'two_pages_behind': None
            },
            'paginator': None
        }

    page, paginator = paginators_params(request, content, count)

    # Расчет диапазона для стрелок (с проверкой на выход за границы)
    two_pages_ahead = min(page.number + 2, paginator.num_pages)
    two_pages_behind = max(page.number - 2, 1)

    # Проверка наличия страниц для стрелок
    arrows_left_border = paginator.page(two_pages_behind) if two_pages_behind < page.number else None
    arrows_right_border = paginator.page(two_pages_ahead) if two_pages_ahead > page.number else None

    left_switch = two_pages_behind < page.number
    right_switch = two_pages_ahead > page.number

    # Проверка текущей страницы
    is_first_page = page.number == 1
    is_last_page = page.number == paginator.num_pages

    # Подготовка параметров для вывода
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

def get_tags_per_question(questions):
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
