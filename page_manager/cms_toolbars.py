from cms.extensions.toolbar import ExtensionToolbar
from cms.toolbar_pool import toolbar_pool
from page_manager.models import MetaTagsExtension


@toolbar_pool.register
class IconExtensionToolbar(ExtensionToolbar):
    model = MetaTagsExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if current_page_menu:
            page_extension, url = self.get_page_extension_admin()
            if url:
                current_page_menu.add_modal_item("Zawartość SEO", url=url)
