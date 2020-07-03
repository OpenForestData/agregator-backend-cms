import json

from page_manager.models import MainPage, AccordionPage, AboutUsPage


def get_proper_template_info(page):
    template = page.extended_fields.first()
    if template:
        if not template.about_us_id == None:
            return list(AboutUsPage.objects.filter(pk=template.about_us_id).values())
        if not template.accordion_id == None:
            return list(AccordionPage.objects.filter(pk=template.accordion_id).values())
        if not template.main_id == None:
            return list(MainPage.objects.filter(pk=template.main_id).values())
    return {}
