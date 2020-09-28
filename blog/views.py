from cms.utils import get_language_from_request
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from blog.models import Article, BlogFront, BlogKeyword


def detail(request, slug):
    """
    Endpoint responsible ofr getting article details and related
    articles data
    :param request: request
    :param slug: slug: str
    :return: response: JsonResponse
    """
    retlated_posts = []
    articles_queryset = Article.objects.filter(slug=slug)
    if len(articles_queryset) > 0:
        first_article = articles_queryset.first()
        related_queryset = Article.objects.filter(keywords__in=list(first_article.keywords.all()))
        for related in related_queryset:
            retlated_posts.append(related.get_content())
        return JsonResponse({'article': first_article.get_content(), 'related_posts': retlated_posts},
                            safe=False)
    return redirect(reverse('api:blog:index'))


def latest(request):
    """
    Endpoint responsible for redirect to latest article (newest)
    :param request: request
    :return: None
    """
    article = Article.objects.all().order_by('date').first()
    return redirect(reverse('blog:detail', kwargs={'slug': article.slug}), safe=False)


def index(request):
    """
    Endpoint for Main blog index page - list of all articles
    :param request: request
    :return: JsonResponse
    """
    language = get_language_from_request(request)
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 6)
    keywords_slug = request.GET.get('keyword', None)
    current_page = list(BlogFront.objects.all().values())
    keywords_set = BlogKeyword.objects.get_by_lang(language)
    keywords = []
    for article_keyword in keywords_set:
        keywords.append({
            'title': article_keyword.title,
            'url': article_keyword.get_absolute_url(),
            'slug': article_keyword.slug
        })

    articles_queryset = Article.objects.get_by_lang(language).order_by('-date')
    if keywords_slug:
        blog_keyword = BlogKeyword.objects.filter(slug=keywords_slug, language=language).first()
        if blog_keyword:
            articles_queryset = blog_keyword.get_articles()
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
            'offset': {'count': paginator.count, 'per_page': paginator.per_page, 'num_pages': paginator.num_pages},
            'current_page': current_page,
            'keywords': keywords
        },
        safe=False)


def keyword(request, slug):
    """
    Endpoint responsible for obtaining articles associated
    with keyword based on keyword's slug
    :param request: request
    :param slug: slug: str
    :return: JsonResponse
    """
    blog_keyword = BlogKeyword.objects.get(slug=slug)
    all_articles = Article.objects.all()
    articles = []
    articles_queryset = all_articles.filter(keywords=blog_keyword).order_by('date')
    for article in articles_queryset:
        articles.append(article.get_content())
    current_page = list(BlogFront.objects.all().values())
    keywords_set = BlogKeyword.objects.all()
    keywords = []
    for article_keyword in keywords_set:
        keywords.append({
            'title': article_keyword.title,
            'url': article_keyword.get_absolute_url()
        })
    return JsonResponse({'articles': articles, 'current_page': current_page, 'keywords': keywords}, safe=False)
