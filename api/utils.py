import json

from cms.models import Page

from page_manager.models import MainPage, AccordionPage, AboutUsPage, PagePattern


def get_proper_template_info(page):
    template = page.
    if template:
        if not template.about_us_id == None:
            return list(AboutUsPage.objects.filter(pk=template.about_us_id).values())
        if not template.accordion_id == None:
            return list(AccordionPage.objects.filter(pk=template.accordion_id).values())
        if not template.main_id == None:
            return list(MainPage.objects.filter(pk=template.main_id).values())
    return {}
