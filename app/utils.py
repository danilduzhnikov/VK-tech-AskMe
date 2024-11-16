from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import QuestionTag, Tag, Question

def paginations_params(request, content, count):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(content, count)

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

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

def question_tags(question):
    tags = QuestionTag.objects.filter(question=question)
    return Tag.objects.filter(id__in=tags)