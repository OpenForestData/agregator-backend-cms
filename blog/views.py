from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from easy_thumbnails.files import get_thumbnailer

from blog.models import Article, BlogFront, BlogKeword


def detail(request, slug):
    try:
        articles = []
        articles_queryset = Article.objects.filter(slug=slug)
        for article in articles_queryset:
            options = {'size': (1680, 900), 'crop': True}
            try:
                image_in_list_thumb_url = get_thumbnailer(article.image_in_list).get_thumbnail(options).url
            except Exception as ex:
                image_in_list_thumb_url = ""
            options = {'size': (1200, 630), 'crop': True}
            try:
                og_image_thumb_url = get_thumbnailer(article.og_image).get_thumbnail(options).url
            except Exception as ex:
                og_image_thumb_url = ""
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
                'content': article.content,
                'keywords': [{'title': keyword.title, 'url': keyword.get_absolute_url()} for keyword in
                             article.keywords.all()],
                'movie_youtube_link': article.movie_youtube_link,
                'url': article.get_absolute_url()
            })
        return JsonResponse({'article': articles},
                            safe=False)
    except Exception as ex:
        print(str(ex))
    return redirect(reverse('blog:index'))


def latest(request):
    article = Article.objects.all().order_by('date').first()
    return redirect(reverse('blog:detail', kwargs={'slug': article.slug}), safe=False)


def index(request):
    current_page = list(BlogFront.objects.all().values())
    keywords_set = BlogKeword.objects.all()
    keywords = []
    for keyword in keywords_set:
        keywords.append({
            'title': keyword.title,
            'url': keyword.get_absolute_url()
        })

    articles_queryset = Article.objects.all().order_by('date')
    articles = []
    for article in articles_queryset:
        options = {'size': (1680, 900), 'crop': True}
        try:
            image_in_list_thumb_url = get_thumbnailer(article.image_in_list).get_thumbnail(options).url
        except Exception as ex:
            image_in_list_thumb_url = ""
        options = {'size': (1200, 630), 'crop': True}
        try:
            og_image_thumb_url = get_thumbnailer(article.og_image).get_thumbnail(options).url
        except Exception as ex:
            og_image_thumb_url = ""
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
            'keywords': [{'title': keyword.title, 'url': keyword.get_absolute_url()} for keyword in
                         article.keywords.all()],
            'movie_youtube_link': article.movie_youtube_link,
            'url': article.get_absolute_url()
        })

    return JsonResponse({'articles': articles, 'current_page': current_page, 'keywords': keywords}, safe=False)


def keyword(request, slug):
    blog_keyword = BlogKeword.objects.get(slug=slug)
    all_articles = Article.objects.all()
    articles = []
    articles_queryset = all_articles.filter(keywords=blog_keyword).order_by('date')
    for article in articles_queryset:
        options = {'size': (1680, 900), 'crop': True}
        try:
            image_in_list_thumb_url = get_thumbnailer(article.image_in_list).get_thumbnail(options).url
        except Exception as ex:
            image_in_list_thumb_url = ""
        options = {'size': (1200, 630), 'crop': True}
        try:
            og_image_thumb_url = get_thumbnailer(article.og_image).get_thumbnail(options).url
        except Exception as ex:
            og_image_thumb_url = ""
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
            'keywords': [{'title': keyword.title, 'url': keyword.get_absolute_url()} for keyword in
                         article.keywords.all()],
            'movie_youtube_link': article.movie_youtube_link,
            'url': article.get_absolute_url()
        })
    current_page = list(BlogFront.objects.all().values())
    keywords_set = BlogKeword.objects.all()
    keywords = []
    for keyword in keywords_set:
        keywords.append({
            'title': keyword.title,
            'url': keyword.get_absolute_url()
        })
    return JsonResponse({'articles': articles, 'current_page': current_page, 'keywords': keywords}, safe=False)
