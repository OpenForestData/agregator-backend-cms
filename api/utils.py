from cms.models import Page


def get_proper_template_content(page: Page, language: str):
    """
    Function responsible for getting proper template based
    on page title received from url
    :param page: Page class object
    :param language: alpha-2 language code
    :return: dict
    """
    template = page.title_set.filter(language=language).first().page_patterns.first()
    if template:
        return template.get_page_pattern_data()
    return {}
