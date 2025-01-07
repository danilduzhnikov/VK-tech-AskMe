from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import QuestionTag, Tag, QuestionLike
from django.db.models import Count

# Стартовые свойства пагинатора
def paginators_params(request, content, count):
    """
    Возвращает текущую страницу и пагинатор.
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
    Расширенная версия пагинации с дополнительными параметрами.
    """
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
                'two_pages_behind': None,
            },
            'paginator': None
        }

    # Получение базовых данных пагинации
    page, paginator = paginators_params(request, content, count)

    # Расчет параметров стрелок
    two_pages_ahead = min(page.number + 2, paginator.num_pages)
    two_pages_behind = max(page.number - 2, 1)

    left_switch = two_pages_behind < page.number
    right_switch = two_pages_ahead > page.number

    is_first_page = page.number == 1
    is_last_page = page.number == paginator.num_pages

    params = {
        'page_obj': page,
        'paginator': paginator,
        'left_switch': left_switch,
        'right_switch': right_switch,
        'is_first_page': is_first_page,
        'is_last_page': is_last_page,
        'arrows_left_border': two_pages_behind if left_switch else None,
        'arrows_right_border': two_pages_ahead if right_switch else None,
        'two_pages_ahead': two_pages_ahead,
        'two_pages_behind': two_pages_behind,
    }

    return {
        'page_objects': page.object_list,
        'params': params,
        'paginator': paginator,
    }


def get_tags_per_question(questions, user=None):
    """
    Получение тегов и количества лайков для одного или нескольких вопросов,
    а также информации о том, лайкал ли их пользователь.

    :param questions: Список или одиночный вопрос (объект Question).
    :param user: Пользователь, для которого проверяется, лайкал ли вопрос.
    :return: Список словарей с информацией о вопросах, тегах, лайках и лайкнул ли пользователь вопрос.
    """
    if not isinstance(questions, list):
        questions = [questions]

    # Получаем IDs вопросов
    question_ids = [question.id for question in questions]

    # Получаем записи QuestionTag, связанные с этими вопросами
    question_tag_records = QuestionTag.objects.filter(question_id__in=question_ids)

    # Группируем теги по question_id
    tags_by_question_id = {}
    for record in question_tag_records:
        if record.question_id not in tags_by_question_id:
            tags_by_question_id[record.question_id] = []
        tags_by_question_id[record.question_id].append(record.tag_id)

    # Извлекаем все уникальные теги одним запросом
    tag_ids = set(tag_id for tag_list in tags_by_question_id.values() for tag_id in tag_list)
    tags = Tag.objects.filter(id__in=tag_ids)

    # Преобразуем теги в словарь для быстрого доступа
    tags_dict = {tag.id: tag for tag in tags}

    # Получаем количество лайков для каждого вопроса
    likes = (
        QuestionLike.objects.filter(question_id__in=question_ids)
        .values('question_id')
        .annotate(like_count=Count('id'))
    )

    # Преобразуем количество лайков в словарь {question_id: like_count}
    likes_dict = {like['question_id']: like['like_count'] for like in likes}

    # Если user передан, получаем лайкнул ли пользователь каждый вопрос
    if user:
        user_likes_dict = {
            like.question_id: True
            for like in QuestionLike.objects.filter(question_id__in=question_ids, user_id=user.id)
        }
    else:
        # Если пользователя нет, ставим для всех вопросов "is_liked" как "false"
        user_likes_dict = {question_id: False for question_id in question_ids}

    # Формируем список словарей с результатами
    question_tags = [
        {
            'question': question,
            'tags': [tags_dict[tag_id] for tag_id in tags_by_question_id.get(question.id, [])],
            'likes_count': likes_dict.get(question.id, 0),  # Если лайков нет, подставляем 0
            'is_liked': 'true' if user_likes_dict.get(question.id, False) else 'false'
        }
        for question in questions
    ]

    return question_tags

# Struct of question_tags for context
# [
#     {
#         'question': <Question 1>,
#         'tags': [<Tag 1>, <Tag 2>],
#         'likes_count': 5,
#         'is_liked': True
#     },
#     {
#         'question': <Question 2>,
#         'tags': [<Tag 3>],
#         'likes_count': 0,
#         'is_liked': False
#     }
# ]
