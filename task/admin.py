from django.contrib import admin
from amortization.task.models import Firm

class FirmAdmin(admin.ModelAdmin):
    list_display = ('name', 'for_print')
    ordering = ['name', ]

admin.site.register(Firm, FirmAdmin)