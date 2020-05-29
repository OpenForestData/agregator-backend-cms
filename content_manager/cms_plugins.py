from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from content_manager.admin import SlideInlineAdmin
from content_manager.models import SliderPlugin, Slide


@plugin_pool.register_plugin
class SliderFrontPlugin(CMSPluginBase):
    """
    Main slider plugin used on main site
    """
    model = SliderPlugin
    name = "Slider Główny"
    render_template = "content_manager/slider/main.html"
    inlines = (SlideInlineAdmin,)

    def render(self, context, instance, placeholder):
        context.update({
            'slides': instance.slides.all(),
        })
        return context
