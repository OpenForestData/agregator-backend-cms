from cms.cms_menus import CMSMenu
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import FacetField
from menus.menu_pool import menu_pool


def facet_list(request):
    all_facets = FacetField.objects.all().order_by('order').values('facet_field_name', 'facet_field_friendly_name')
    return JsonResponse(list(all_facets), safe=False)


def global_data(request):
    """
    Endpoint responsible for providing basic 'each view'
    data for frontend
    :param request: request
    :return: Json data
    """
    response = {
        'menu': []
    }
    pages = menu_pool.get_renderer(request).get_nodes(request)
    for page in pages:
        response['menu'].append({
            'id': page.id,
            'title': page.title,
            'attr': page.attr,
            'parent_id': page.parent_id
        })
    return JsonResponse(response, safe=False)


def get_page_details(request, page_id):
    return JsonResponse({})


@csrf_exempt
def populate_categories_fields_list(request):
    if request.POST:
        categories_to_populate = request.POST.getlist('category')
    return JsonResponse({})


def get_categories_fields_list(request):
    return JsonResponse({})


@csrf_exempt
def ragister_metadata_blocks(request):
    return JsonResponse({})
