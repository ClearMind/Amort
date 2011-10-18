from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Employee(models.Model):
    fio = models.CharField(max_length=128, verbose_name=_('fio'))
    tab_number = models.IntegerField(verbose_name=_("Tabel number"))
    post = models.CharField(max_length=32, verbose_name=_('Post'))
    cabinet = models.CharField(max_length=5, verbose_name=_('Cabinet'))
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.fio

    class Meta:
        db_table = 'account_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
