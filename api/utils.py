from cms.models import Title
from easy_thumbnails.files import get_thumbnailer
from page_manager.models import AccordionPage, AboutUsPage, Accordion


def get_proper_template_info(page, language):
    template = page.title_set.filter(language=language).first().page_patterns.first()
    if template:
        return template.get_json_data()
    return {}
