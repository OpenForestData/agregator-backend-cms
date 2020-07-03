import json

from easy_thumbnails.files import get_thumbnailer

from page_manager.models import MainPage, AccordionPage, AboutUsPage, Accordion, IconSpecies, FaqShort


def get_proper_template_info(page):
    from page_manager.models import PagePattern
    template = None
    page_patterns = PagePattern.objects.all()
    for page_pattern in page_patterns:
        # TODO: could not found why pages are duplicated and how to create
        # relations without this trick
        if str(page_pattern.page) == str(page):
            template = page_pattern
    if template:
        if not template.about_us_id == None:
            about_page = AboutUsPage.objects.filter(pk=template.about_us_id).first()
            options = {'size': (1200, 630), 'crop': True}
            try:
                og_image_thumb_url = get_thumbnailer(about_page.og_image).get_thumbnail(options).url
            except Exception as ex:
                og_image_thumb_url = ""
            return {
                'title_seo': about_page.title_seo,
                'description': about_page.description,
                'keywords_seo': about_page.keywords_seo,
                'author': about_page.author,
                'og_type': about_page.og_type,
                'og_image': og_image_thumb_url,
                'title': about_page.title,
                'content': about_page.content,
            }

        if not template.accordion_id == None:
            accordion_page = AccordionPage.objects.filter(pk=template.accordion_id).first()

            options = {'size': (1200, 630), 'crop': True}
            try:
                og_image_thumb_url = get_thumbnailer(accordion_page.og_image).get_thumbnail(options).url
            except Exception as ex:
                og_image_thumb_url = ""
            return {
                'title_seo': accordion_page.title_seo,
                'description': accordion_page.description,
                'keywords_seo': accordion_page.keywords_seo,
                'author': accordion_page.author,
                'og_type': accordion_page.og_type,
                'og_image': og_image_thumb_url,
                'title': accordion_page.title,
                'content': accordion_page.content,
                'accordions': [{'title': accordion.title, 'content': accordion.content} for accordion in
                               Accordion.objects.filter(accordion_page=accordion_page).order_by('order')]
            }
        if not template.main_id == None:
            pass
    return {}
