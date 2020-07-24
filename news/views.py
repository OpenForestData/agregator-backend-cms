from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from easy_thumbnails.files import get_thumbnailer

from news.models import News, NewsFront


def detail(request, slug):
    try:
        article = {}
        articles_queryset = News.objects.filter(slug=slug)
        for article in articles_queryset:
            options = {'size': (1680, 900), 'crop': True}
            image_in_list_thumb_url = ""
            og_image_thumb_url = ""
            try:
                image_in_list_thumb_url = get_thumbnailer(article.image_in_list).get_thumbnail(options).url
            except Exception as ex:
                print(ex)
            try:
                og_image_thumb_url = get_thumbnailer(article.og_image).get_thumbnail(options).url
            except Exception as ex:
                print(ex)
            article = {
                'title_seo': article.title_seo,
                'description': article.description,
                'keywords_seo': article.keywords_seo,
                'author': article.author,
                'og_type': article.og_type,
                'og_image': og_image_thumb_url,
                'image_in_list': image_in_list_thumb_url,
                'title': article.title,
                'date': article.date,
                'content': article.content,
                'url': article.get_absolute_url(),
                'slug': article.slug
            }
        return JsonResponse({'article': article},
                            safe=False)
    except Exception as ex:
        print(ex)
    return redirect(reverse('api:news:index'))


def latest(request):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 6)
    current_page = list(NewsFront.objects.all().values())
    articles_queryset = News.objects.all().order_by('date')
    articles = []
    for article in articles_queryset:
        options = {'size': (1680, 900), 'crop': True}
        image_in_list_thumb_url = ""
        og_image_thumb_url = ""
        try:
            image_in_list_thumb_url = get_thumbnailer(article.image_in_list).get_thumbnail(options).url
        except Exception as ex:
            print(ex)
        try:
            og_image_thumb_url = get_thumbnailer(article.og_image).get_thumbnail(options).url
        except Exception as ex:
            print(ex)

        next_article, prev_article = article.next_prev_get()
        articles.append({
            'title_seo': article.title_seo,
            'description': article.description,
            'keywords_seo': article.keywords_seo,
            'author': article.author,
            'og_type': article.og_type,
            'og_image': og_image_thumb_url,
            'image_in_list': image_in_list_thumb_url,
            'title': article.title,
            'date': article.date,
            'desc': article.desc,
            'url': article.get_absolute_url(),
            'slug': article.slug,
            'next': next_article.slug,
            'prev': prev_article.slug
        })
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
        },
        safe=False)
