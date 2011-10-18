
__author__ = 'cm'

from django.utils.translation import ugettext_lazy as _
from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('Menu item name'))
    url = models.CharField(max_length=128, verbose_name=_('Location address'))
    description = models.TextField(verbose_name=_('Menu item description'), blank=True, null=True)
    order = models.IntegerField(verbose_name=_('Order'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu items')
  