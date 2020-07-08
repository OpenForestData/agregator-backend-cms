import json
from cms.models import TreeNode, LanguageError, settings, get_cms_setting
from cms.page_rendering import _render_welcome_page, _handle_no_page
from cms.toolbar.utils import get_toolbar_from_request
from cms.utils import get_current_site, get_language_list, get_language_from_request
from cms.utils.i18n import get_public_languages, get_redirect_on_fallback, get_default_language_for_site, \
    get_fallback_languages
from cms.utils.page import get_page_from_request
from cms.views import _clean_redirect_url
from django.contrib.auth.views import redirect_to_login
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt
from easy_thumbnails.files import get_thumbnailer
from api.data_populator import DataPopulator
from api.models import FilterGroup, AgregatorCategory, AdvancedSearchFilterGroup
from menus.menu_pool import menu_pool
from api.utils import get_proper_template_info
from core.settings import CMS_LANGUAGES
from page_manager.models import MainPage, IconSpecies, FaqShort


def facet_list(request):
    all_facets = {'basic_filters': {}, 'advanced_search_filters': {}}
    for field_group in FilterGroup.objects.all().order_by('order'):
        all_facets['basic_filters'][field_group.name] = {
            'friendly_name': field_group.friendly_name,
            'id': field_group.id,
            'fields': field_group.get_fields()
        }
    for field_group in AdvancedSearchFilterGroup.objects.all().order_by('order'):
        all_facets['advanced_search_filters'][field_group.name] = {
            'friendly_name': field_group.friendly_name,
            'id': field_group.id,
            'fields': field_group.get_fields()
        }
    return JsonResponse(all_facets, safe=False)


def menu(request):
    """
    Endpoint responsible for providing basic 'each view'
    data for frontend
    :param request: request
    :return: Json data
    """

    response = {
        'menu': {}
    }

    for lang in CMS_LANGUAGES[1]:
        lang_code = lang['code']
        response['menu'][lang_code] = []
        request.COOKIES['django_language'] = lang['code']
        pages = menu_pool.get_renderer(request).get_nodes(request)
        for page in pages:
            response['menu'][lang_code].append({
                'id': page.id,
                'title': page.title,
                'attr': page.attr,
                'parent_id': page.parent_id,
                'url': 'pages?slug=' + page.get_absolute_url(),
                'slug': page.path
            })
    return JsonResponse(response, safe=False)


def page_details(request, slug):
    # Get a Page model object from the request
    site = get_current_site()
    page = get_page_from_request(request, use_path=slug)
    toolbar = get_toolbar_from_request(request)
    tree_nodes = TreeNode.objects.get_for_site(site)

    if not page and not slug and not tree_nodes.exists():
        # render the welcome tree if the requested path is root "/"
        # and there's no pages
        return _render_welcome_page(request)

    if not page:
        # raise 404
        return HttpResponse(status=404, content='Page not Found')

    request.current_page = page

    if hasattr(request, 'user') and request.user.is_staff:
        user_languages = get_language_list(site_id=site.pk)
    else:
        user_languages = get_public_languages(site_id=site.pk)

    request_language = get_language_from_request(request)

    if not page.is_home and request_language not in user_languages:
        # The homepage is treated differently because
        # when a request goes to the root of the site (/)
        # without a language, Django will redirect to the user's
        # browser language which might not be a valid cms language,
        # this means we need to correctly redirect that request.
        return _handle_no_page(request)

    # get_published_languages will return all languages in draft mode
    # and published only in live mode.
    # These languages are then filtered out by the user allowed languages
    available_languages = [
        language for language in user_languages
        if language in list(page.get_published_languages())
    ]

    own_urls = [
        request.build_absolute_uri(request.path),
        '/%s' % request.path,
        request.path,
    ]

    try:
        redirect_on_fallback = get_redirect_on_fallback(request_language, site_id=site.pk)
    except LanguageError:
        redirect_on_fallback = False

    if request_language not in user_languages:
        # Language is not allowed
        # Use the default site language
        default_language = get_default_language_for_site(site.pk)
        fallbacks = get_fallback_languages(default_language, site_id=site.pk)
        fallbacks = [default_language] + fallbacks
    else:
        fallbacks = get_fallback_languages(request_language, site_id=site.pk)

    # Only fallback to languages the user is allowed to see
    fallback_languages = [
        language for language in fallbacks
        if language != request_language and language in available_languages
    ]
    language_is_unavailable = request_language not in available_languages

    if language_is_unavailable and not fallback_languages:
        # There is no tree with the requested language
        # and there's no configured fallbacks
        return _handle_no_page(request)
    elif language_is_unavailable and (redirect_on_fallback or page.is_home):
        # There is no tree with the requested language and
        # the user has explicitly requested to redirect on fallbacks,
        # so redirect to the first configured / available fallback language
        fallback = fallback_languages[0]
        redirect_url = page.get_absolute_url(fallback, fallback=False)
    else:
        page_path = page.get_absolute_url(request_language)
        page_slug = page.get_path(request_language) or page.get_slug(request_language)

        if slug and slug != page_slug and request.path[:len(page_path)] != page_path:
            # The current language does not match its slug.
            # Redirect to the current language.
            return HttpResponseRedirect(page_path)
        # Check if the tree has a redirect url defined for this language.
        redirect_url = page.get_redirect(request_language, fallback=False) or ''
        redirect_url = _clean_redirect_url(redirect_url, request_language)

    if redirect_url:
        if request.user.is_staff and toolbar.edit_mode_active:
            toolbar.redirect_url = redirect_url
        elif redirect_url not in own_urls:
            # prevent redirect to self
            return HttpResponseRedirect(redirect_url)

    # permission checks
    if page.login_required and not request.user.is_authenticated:
        return redirect_to_login(urlquote(request.get_full_path()), settings.LOGIN_URL)

    if hasattr(request, 'toolbar'):
        request.toolbar.set_object(page)

    # structure_requested = get_cms_setting('CMS_TOOLBAR_URL__BUILD') in request.GET

    return JsonResponse(get_proper_template_info(page), safe=False)


@csrf_exempt
def populate_categories_fields_list(request):
    """
    Endpoint responsible for populating categories based on
    agregator registered data
    :param request: request
    :return: 200, 400
    """
    if request.POST:
        categories_to_populate = request.POST.get('categories_fields_list', None)
        if categories_to_populate:
            data_populator = DataPopulator()
            successfully_populated = data_populator.populate_categories(categories_to_populate)
            if successfully_populated:
                return HttpResponse('Properly populated categories')
    return HttpResponse(
        'Could not populate categories', status=400)


def get_categories_fields_list(request):
    public_categories = {}
    for category in AgregatorCategory.objects.filter(public=True).order_by('order'):
        public_categories[category.name] = {
            'name': category.name,
            'friendly_name': category.friendly_name,
            'id': category.id,
            'description': category.description,
            'dvName': category.dv_name,
            'publicationDate': category.publication_date,
            'dvAffiliation': category.dv_affiliation
        }
    return JsonResponse(public_categories, safe=False)


@csrf_exempt
def ragister_metadata_blocks(request):
    if request.POST:
        metadata_json_string = request.POST.get('metadata_blocks', None)
        if metadata_json_string:
            try:
                metadata_blocks = json.loads(metadata_json_string)
                data_populator = DataPopulator()
                successfully_populated = data_populator.populate_metadata_blocks(metadata_blocks)
                return HttpResponse('Properly populated metadata blocks') if successfully_populated else HttpResponse(
                    'Could not populate metadata blocks', status=400)
            except Exception as ex:
                print(ex)
    return HttpResponse('Something went wrong', status=400)


def home(request):
    main_page = MainPage.objects.first()
    try:
        options = {'size': (1200, 630), 'crop': True}
        og_image_thumb_url = get_thumbnailer(main_page.og_image).get_thumbnail(options).url
    except Exception as ex:
        print(ex)
        og_image_thumb_url = ""
    try:
        options = {'size': (1680, 900), 'crop': True}
        mobile_app_image = get_thumbnailer(main_page.mobile_app_image).get_thumbnail(options).url
    except Exception:
        print(ex)
        mobile_app_image = ""
    return JsonResponse({
        'title_seo': main_page.title_seo,
        'description': main_page.description,
        'keywords_seo': main_page.keywords_seo,
        'author': main_page.author,
        'og_type': main_page.og_type,
        'og_image': og_image_thumb_url,
        'title_slider': main_page.title_slider,
        'title_slider_small': main_page.title_slider_small,
        'contact_content': main_page.contact_content,
        'youtube_title': main_page.youtube_title,
        'youtube_link': main_page.youtube_link,
        'youtube_mobie_text': main_page.youtube_mobie_text,
        'mobile_app_title': main_page.mobile_app_title,
        'mobile_app_content': main_page.mobile_app_content,
        'mobile_app_image': mobile_app_image,
        'mobile_app_cta_link': main_page.mobile_app_cta_link,
        'mobile_app_cta_text': main_page.mobile_app_cta_text,
        'categories': [{'title': category.title, 'image': category.image} for category in
                       IconSpecies.objects.filter(main_page=main_page).order_by('order')],
        'faqs': [{'title': faq.title, 'url': faq.anchor} for faq in
                 FaqShort.objects.filter(main_page=main_page).order_by('order')]
    }, safe=False)

#
# def initialize_static_filters():
#     #TODO not good place for that1
