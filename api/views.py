import json

from cms.cms_menus import CMSMenu
from cms.models import Page
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from api.data_populator import DataPopulator
from api.models import FilterGroup, AgregatorCategory, AdvancedSearchFilterGroup
from menus.menu_pool import menu_pool

from core.settings import CMS_LANGUAGES


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
            })
    return JsonResponse(response, safe=False)


def page_details(request, page_id: int, lang_code: str):
    return JsonResponse({})


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

#
# def initialize_static_filters():
#     #TODO not good place for that1
