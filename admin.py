from models import MenuItem

__author__ = 'cm'

from django.contrib.admin import ModelAdmin
from django.contrib.admin import site

class MenuItemAdmin(ModelAdmin):
    list_display = ("order", "name", "url", 'for_staff')
    ordering = ["order"]

site.register(MenuItem, MenuItemAdmin)
  