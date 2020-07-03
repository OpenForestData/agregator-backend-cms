from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from blog.models import Article

@plugin_pool.register_plugin
class BlogSection(CMSPluginBase):
    """
    Main section for blog posts
    """
    name = "Ostatnie 3 posty"
    render_template = "blog/3_posts_section.html"

    def render(self, context, instance, placeholder):
        context.update({
            'last_posts': Article.objects.all().order_by('date')[:3],
        })
        return context
