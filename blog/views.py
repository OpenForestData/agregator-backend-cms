from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from blog.models import Article, BlogFront, BlogKeword


def detail(request, slug):
    try:
        article = list(Article.objects.filter(slug=slug).values())
        return JsonResponse({'article': article, 'current_page': article})
    except Exception as ex:
        print(str(ex))
    return redirect(reverse('blog:index'))


def latest(request):
    article = Article.objects.all().order_by('date').first()
    return redirect(reverse('blog:detail', kwargs={'slug': article.slug}))


def index(request):
    current_page = list(BlogFront.objects.all().values())
    keywords = list(BlogKeword.objects.all().values())
    articles = list(Article.objects.all().order_by('date').values())
    return JsonResponse({'articles': articles, 'current_page': current_page, 'keywords': keywords}, safe=False)


def keyword(request, slug):
    blog_keyword = BlogKeword.objects.get(slug=slug)
    all_articles = Article.objects.all()
    articles = list(all_articles.filter(keywords=blog_keyword).order_by('date').values())
    current_page = list(BlogFront.objects.all().values())
    keywords = list(BlogKeword.objects.all())
    return JsonResponse({'articles': articles, 'current_page': current_page, 'keywords': keywords})
