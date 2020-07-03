from xmlrpc.client import DateTime

from cms.api import create_page
from cms.models import Page
from django.utils.text import slugify

from api.models import FilterGroup, FilterField, AdvancedSearchFilterGroup, AdvancedSearchFilterField
from blog.models import BlogKeword, Article
from page_manager.models import AccordionPage, PagePattern, Accordion, AboutUsPage, MainPage, IconSpecies, FaqShort

BASIC_FILTERS = [{
    'name': "geospatial", 'friendly_name': "Geo Spatial",
    'fields': [
        {'name': "geographicBoundingBox", 'displayName': "Geographic Bounding Box", 'title': "Geographic Bounding Box",
         'type': "MAP", 'description': "Description"}],
}, {
    'name': "darwincore", 'friendly_name': "Darwin Core Metadata",
    'fields': [
        {'name': "dwcEventTime", 'displayName': "Date Range Test", 'title': "Date Range Test",
         'type': "DATERANGE", 'description': "Date range Description"},
    ],
}]


def create_static_basic_filters_fields():
    for basic_filter in BASIC_FILTERS:
        filter_group = FilterGroup.objects.create(
            name=basic_filter['name'],
            friendly_name=basic_filter['friendly_name']
        )
        for field_data in basic_filter['fields']:
            FilterField.objects.create(
                field_name=field_data['name'],
                friendly_name=field_data['displayName'],
                title=field_data['title'],
                type=field_data['type'],
                description=field_data['description'],
                filter_group=filter_group,
                public=True
            )

        filter_group = AdvancedSearchFilterGroup.objects.create(
            name=basic_filter['name'],
            friendly_name=basic_filter['friendly_name']
        )
        for field_data in basic_filter['fields']:
            AdvancedSearchFilterField.objects.create(
                field_name=field_data['name'],
                friendly_name=field_data['displayName'],
                title=field_data['title'],
                type=field_data['type'],
                description=field_data['description'],
                filter_group=filter_group,
                public=True
            )
    return True


def create_basic_templates_data():
    page = create_page('Test Akordion', 'fullwidth.html', 'pl', 'Test')
    page.publish('pl')

    accordion_page = AccordionPage(**{
        'title': "Test",
        'title_seo': "Test seo",
        'description': "Test desc seo",
        'keywords_seo': "Test keyword seo",
        'author': "Autor Seo",
        'og_type': 'type og seo',
        'content': "To jest content testowy"
    })
    accordion_page.save()

    for _ in range(0, 10):
        Accordion.objects.create(**{
            'accordion_page': accordion_page,
            'title': "Test",
            'content': "To jest content testowy",

        })

    PagePattern.objects.create(page=page, accordion=accordion_page)

    page = create_page('Test O nas', 'fullwidth.html', 'pl', 'Test')
    page.publish('pl')

    about_us_page = AboutUsPage(**{
        'title': "Test",
        'title_seo': "Test seo",
        'description': "Test desc seo",
        'keywords_seo': "Test keyword seo",
        'author': "Autor Seo",
        'og_type': 'type og seo',
        'content': "To jest content testowy"
    })
    about_us_page.save()
    PagePattern.objects.create(page=page, about_us=about_us_page)

    page = create_page('Test Strona główna', 'fullwidth.html', 'pl', 'Test')
    page.publish('pl')

    main_page = MainPage(**{
        'title': "Test",
        'title_seo': "Test seo",
        'description': "Test desc seo",
        'keywords_seo': "Test keyword seo",
        'author': "Autor Seo",
        'og_type': 'type og seo',
        'title_slider': "Tytuł slidera duży",
        'title_slider_small': "Tytuł sldiera mały",
        'contact_content': "Content dla sekcji kontakt",
        'youtube_title': "Tytuł youtube",
        'youtube_link': "https://www.youtube.com/watch?v=QcXtF8Gj_Z0",
        'youtube_mobie_text': "Tekst pod filmem",
        'mobile_app_title': "Tytuł sekcji aplikacja mobilna",
        'mobile_app_content': "<p>Content dla sekcji mobile</p>",
        'mobile_app_cta_link': "#",
        'mobile_app_cta_text': "Tekst na buttonie"
    })
    main_page.save()

    for _ in range(1, 7):
        IconSpecies.objects.create(main_page=main_page, title=f'test{_}')

    for _ in range(1, 5):
        FaqShort.objects.create(main_page=main_page, title=f'test{_}')

    PagePattern.objects.create(page=page, main=main_page)


def create_basic_articles_and_keyword():
    for _ in range(1, 30):
        BlogKeword.objects.create(**{
            'title': f'Keyword testowy nr {_}',
            'slug': f'keyword-{_}'
        })

    for _ in range(1, 30):
        article = Article(**{
            'title': f"Test {_}",
            'title_seo': "Test seo",
            'description': "Test desc seo",
            'keywords_seo': "Test keyword seo",
            'author': "Autor Seo",
            'og_type': 'type og seo',
            'desc': '<p> OPIST LISTY W jaki sposób się wyróżnić, by przyciągnąć jak największą liczbę odbiorców? Jak wiesz, <strong></strong>, w dzisiejszych czasach praktycznie każda firma, oferująca swoje usługi, ma bardzo wielu konkurentów. Rynek handlu, sprzedaży towarów i usług bardzo się rozszerzył. O wiele trudniej jest się wyróżnić i przyciągnąć uwagę klienta tak, by został on „na dłużej” wierny marce. Dziś liczy się zatem kreatywność i oryginalność, nic więc dziwnego, że wielu przedsiębiorców decyduje się na personalizowanie swoich usług. Na czym zatem polega personalizacja i dlaczego warto ją wykorzystać? <strong></strong> Gotowy?</p>',
            'content': 'CONTENT PO WEJSCIU DO BLOGA W jaki sposób się wyróżnić, by przyciągnąć jak największą liczbę odbiorców? Jak wiesz, <strong></strong>, w dzisiejszych czasach praktycznie każda firma, oferująca swoje usługi, ma bardzo wielu konkurentów. Rynek handlu, sprzedaży towarów i usług bardzo się rozszerzył. O wiele trudniej jest się wyróżnić i przyciągnąć uwagę klienta tak, by został on „na dłużej” wierny marce. Dziś liczy się zatem kreatywność i oryginalność, nic więc dziwnego, że wielu przedsiębiorców decyduje się na personalizowanie swoich usług. Na czym zatem polega personalizacja i dlaczego warto ją wykorzystać? <strong></strong> Gotowy?</p>',
            'movie_youtube_link': 'https://www.youtube.com/watch?v=QcXtF8Gj_Z0',
            'slug': slugify(f'Test {_}')
        })
        article.save()
        article.keywords.add(BlogKeword.objects.get(pk=_))
        article.save()
