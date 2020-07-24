from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from easy_thumbnails.files import get_thumbnailer
from blog.models import Article, BlogFront, BlogKeword
from django.core.paginator import Paginator


def detail(request, slug):
    try:
        article = {}
        retlated_posts = []
        articles_queryset = Article.objects.filter(slug=slug)
        related_queryset = Article.objects.filter(keywords__in=list(articles_queryset.first().keywords.all()))
        for related in related_queryset:
            options = {'size': (1680, 900), 'crop': True}
            image_in_list_thumb_url = ""
            og_image_thumb_url = ""
            try:
                image_in_list_thumb_url = get_thumbnailer(related.image_in_list).get_thumbnail(options).url
            except Exception as ex:
                print(ex)
            try:
                og_image_thumb_url = get_thumbnailer(related.og_image).get_thumbnail(options).url
            except Exception as ex:
                print(ex)
            next_article, prev_article = related.next_prev_get()
            retlated_posts.append({
                'title_seo': related.title_seo,
                'description': related.description,
                'keywords_seo': related.keywords_seo,
                'author': related.author,
                'og_type': related.og_type,
                'og_image': og_image_thumb_url,
                'image_in_list': image_in_list_thumb_url,
                'title': related.title,
                'date': related.date,
                'content': related.content,
                'keywords': [{'title': keyword.title, 'url': keyword.get_absolute_url(), 'slug': keyword.slug} for
                             keyword in related.keywords.all()],
                'movie_youtube_link': related.movie_youtube_link,
                'url': related.get_absolute_url(),
                'slug': related.slug,
                'related_posts': [],
                'next': next_article.get_absolute_url(),
                'prev': prev_article.get_absolute_url()
            })

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
                'keywords': [{'title': keyword.title, 'url': keyword.get_absolute_url(), 'slug': keyword.slug} for
                             keyword in article.keywords.all()],
                'movie_youtube_link': article.movie_youtube_link,
                'url': article.get_absolute_url(),
                'slug': article.slug,
                'related_posts': [],
                'next': next_article.get_absolute_url(),
                'prev': prev_article.get_absolute_url()
            }
        return JsonResponse({'article': article, 'related_posts': retlated_posts},
                            safe=False)
    except Exception as ex:
        print(ex)
    return redirect(reverse('api:blog:index'))


def latest(request):
    article = Article.objects.all().order_by('date').first()
    return redirect(reverse('blog:detail', kwargs={'slug': article.slug}), safe=False)


def index(request):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 6)
    keywords_slug = request.GET.get('keyword', None)
    current_page = list(BlogFront.objects.all().values())
    keywords_set = BlogKeword.objects.all()
    keywords = []
    for keyword in keywords_set:
        keywords.append({
            'title': keyword.title,
            'url': keyword.get_absolute_url(),
            'slug': keyword.slug
        })

    articles_queryset = Article.objects.all().order_by('date')
    if keywords_slug:
        blog_keyword = BlogKeword.objects.filter(slug=keywords_slug).first()
        if blog_keyword:
            articles_queryset = blog_keyword.get_articles()
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
            'keywords': [{'title': keyword.title, 'url': keyword.get_absolute_url(), 'slug': keyword.slug} for
                         keyword in article.keywords.all()],
            'movie_youtube_link': article.movie_youtube_link,
            'url': article.get_absolute_url(),
            'slug': article.slug
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
            'keywords': keywords
        },
        safe=False)


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
            print(ex)
            image_in_list_thumb_url = ""
        options = {'size': (1200, 630), 'crop': True}
        try:
            og_image_thumb_url = get_thumbnailer(article.og_image).get_thumbnail(options).url
        except Exception as ex:
            print(ex)
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
            'url': article.get_absolute_url(),
            'slug': article.slug
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
