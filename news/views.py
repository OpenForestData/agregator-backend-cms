from cms.utils import get_language_from_request
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from news.models import News, NewsFront


def detail(request, slug):
    """
    Endpoint responsible for getting news details
    :param request: request
    :param slug: slug: str
    :return: JsonResponse
    """
    articles_queryset = News.objects.filter(slug=slug)
    if len(articles_queryset) > 0:
        return JsonResponse({'article': articles_queryset.first().get_content()},
                            safe=False)
    return redirect(reverse('api:news:index'))


def latest(request):
    """
    Endpoint responsible for getting latest news
    :param request: request
    :return: JsonResponse
    """
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 6)
    language = get_language_from_request(request)
    current_page = list(NewsFront.objects.all().values())
    articles_queryset = News.objects.get_by_lang(language).order_by('-date')
    articles = []
    for article in articles_queryset:
        articles.append(article.get_content())
    pagination = Paginator(articles, limit)
    if pagination.count < int(page) or int(page) < 1:
        page = 1
    page_pagination = pagination.page(page)
    paginator = page_pagination.paginator
    return JsonResponse(
        {
            'articles': page_pagination.object_list,
            'offset': {
                'count': paginator.count, 'per_page': paginator.per_page,
                'num_pages': paginator.num_pages
            },
            'current_page': current_page,
        },
        safe=False)
