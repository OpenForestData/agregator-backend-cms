from django.contrib import admin

# Register your models here.
from content_manager.models import Slide


class SlideInlineAdmin(admin.StackedInline):
    model = Slide
