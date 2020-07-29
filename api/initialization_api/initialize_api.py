from cms.api import create_page
from django.utils.text import slugify

from api.models import FilterGroup, FilterField, AdvancedSearchFilterGroup, AdvancedSearchFilterField, AddMenuLinks
from blog.models import BlogKeyword, Article
from news.models import News
from page_manager.models import AccordionPage, Accordion, AboutUsPage, MainPage, IconSpecies, FaqShort

BASIC_LANGUAGES_TO_INITIALIZE_DATA = ['pl', 'en']

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
    models_fields = {'basic': [FilterGroup, FilterField],
                     'advanced': [AdvancedSearchFilterGroup, AdvancedSearchFilterField]}

    for field_type, models_field in models_fields.items():

        for basic_filter in BASIC_FILTERS:
            filter_group = models_field[0].objects.create(
                name=basic_filter['name'],
                friendly_name=basic_filter['friendly_name']
            )
            for field_data in basic_filter['fields']:
                models_field[1].objects.create(
                    field_name=field_data['name'],
                    friendly_name=field_data['displayName'],
                    title=field_data['title'],
                    type=field_data['type'],
                    description=field_data['description'],
                    filter_group=filter_group,
                    public=True if field_type == 'advanced' else False
                )
        return True


def create_basic_templates_data():
    page = create_page('Test Akordion', 'fullwidth.html', 'pl', 'Test Akordion')
    page.publish(language='pl')
    page = create_page('Test Akordion', 'fullwidth.html', 'en', 'Test Akordion EN')
    page.publish(language='en')

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

    # page_pattern = PagePattern.objects.create(page=page, accordion=accordion_page)
    # page_pattern.save()
    # page.publish(language='pl')

    page = create_page('Test O nas', 'fullwidth.html', 'pl', 'Test o nas')

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
    # PagePattern.objects.create(page=page, about_us=about_us_page)
    page.publish(language='pl')

    for lang in BASIC_LANGUAGES_TO_INITIALIZE_DATA:
        main_page = MainPage(**{
            'title': f'Title seo {lang}',
            'language': lang,
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
            IconSpecies.objects.create(main_page=main_page, title=f'test{_}_{lang}')

        for _ in range(1, 5):
            FaqShort.objects.create(main_page=main_page, title=f'test{_}_{lang}', anchor=f'{_}')


def create_basic_articles_and_keyword():
    for _ in range(1, 30):
        BlogKeyword.objects.create(**{
            'title': f'Keyword testowy nr {_}',
            'slug': f'keyword-{_}'
        })

    for _ in range(1, 30):
        for lang in BASIC_LANGUAGES_TO_INITIALIZE_DATA:
            article = Article(**{
                'title': f"Test {_} {lang}",
                'title_seo': "Test seo",
                'description': "Test desc seo",
                'keywords_seo': "Test keyword seo",
                'author': "Autor Seo",
                'og_type': 'type og seo',
                'language': lang,
                'desc': '<p> OPIST LISTY W jaki sposób się wyróżnić, by przyciągnąć jak największą liczbę odbiorców? \
                Jak wiesz, <strong></strong>, w dzisiejszych czasach praktycznie każda firma, oferująca swoje usługi, \
                ma bardzo wielu konkurentów. Rynek handlu, sprzedaży towarów i usług bardzo się rozszerzył. O wiele\
                 trudniej jest się wyróżnić i przyciągnąć uwagę klienta tak, by został on „na dłużej” wierny marce. ]\
                 Dziś liczy się zatem kreatywność i oryginalność, nic więc dziwnego, że wielu przedsiębiorców decyduje \
                 się na personalizowanie swoich usług. Na czym zatem polega personalizacja i dlaczego warto ją wykorzystać?\
                  <strong></strong> Gotowy?</p>',
                'content': 'CONTENT PO WEJSCIU DO BLOGA W jaki sposób się wyróżnić, by przyciągnąć jak największą \
                liczbę odbiorców? Jak wiesz, <strong></strong>, w dzisiejszych czasach praktycznie każda firma, \
                oferująca swoje usługi, ma bardzo wielu konkurentów. Rynek handlu, sprzedaży towarów i usług bardzo \
                się rozszerzył. O wiele trudniej jest się wyróżnić i przyciągnąć uwagę klienta tak, by został on „na \
                dłużej” wierny marce. Dziś liczy się zatem kreatywność i oryginalność, nic więc dziwnego, że wielu \
                przedsiębiorców decyduje się na personalizowanie swoich usług. Na czym zatem polega personalizacja i \
                dlaczego warto ją wykorzystać? <strong></strong> Gotowy?</p>',
                'movie_youtube_link': 'https://www.youtube.com/watch?v=QcXtF8Gj_Z0',
                'slug': slugify(f'Test {_}')
            })
            article.save()
            article.keywords.add(BlogKeyword.objects.get(pk=_))
            article.save()

    for _ in range(1, 30):
        for lang in BASIC_LANGUAGES_TO_INITIALIZE_DATA:
            article = News(**{
                'title': f"Test {_} {lang}",
                'title_seo': "Test seo",
                'description': "Test desc seo",
                'keywords_seo': "Test keyword seo",
                'author': "Autor Seo",
                'language': lang,
                'og_type': 'type og seo',
                'desc': '<p> OPIST LISTY W jaki sposób się wyróżnić, by przyciągnąć jak największą liczbę odbiorców? \
                Jak wiesz, <strong></strong>, w dzisiejszych czasach praktycznie każda firma, oferująca swoje usługi, \
                ma bardzo wielu konkurentów. Rynek handlu, sprzedaży towarów i usług bardzo się rozszerzył. O wiele\
                 trudniej jest się wyróżnić i przyciągnąć uwagę klienta tak, by został on „na dłużej” wierny marce. ]\
                 Dziś liczy się zatem kreatywność i oryginalność, nic więc dziwnego, że wielu przedsiębiorców decyduje \
                 się na personalizowanie swoich usług. Na czym zatem polega personalizacja i dlaczego warto ją wykorzystać?\
                  <strong></strong> Gotowy?</p>',
                'content': 'CONTENT PO WEJSCIU DO BLOGA W jaki sposób się wyróżnić, by przyciągnąć jak największą \
                liczbę odbiorców? Jak wiesz, <strong></strong>, w dzisiejszych czasach praktycznie każda firma, \
                oferująca swoje usługi, ma bardzo wielu konkurentów. Rynek handlu, sprzedaży towarów i usług bardzo \
                się rozszerzył. O wiele trudniej jest się wyróżnić i przyciągnąć uwagę klienta tak, by został on „na \
                dłużej” wierny marce. Dziś liczy się zatem kreatywność i oryginalność, nic więc dziwnego, że wielu \
                przedsiębiorców decyduje się na personalizowanie swoich usług. Na czym zatem polega personalizacja i \
                dlaczego warto ją wykorzystać? <strong></strong> Gotowy?</p>',
                'slug': slugify(f'Test {_}')
            })
            article.save()


def create_small_add_menu():
    for lang in BASIC_LANGUAGES_TO_INITIALIZE_DATA:
        for i in range(1, 3):
            menu_link = AddMenuLinks.objects.create(name=f"Test {i} {lang}", url="#", language=lang)
            print(menu_link.name)
