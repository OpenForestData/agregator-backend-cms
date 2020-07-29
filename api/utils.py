def get_proper_template_info(page, language):
    template = page.title_set.filter(language=language).first().page_patterns.first()
    if template:
        return template.get_json_data()
    return {}
