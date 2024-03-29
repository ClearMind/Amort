# -*- coding: utf-8 -*-

from django.db import models
from amortization.account.models import Employee
from django.utils.translation import ugettext_lazy as _
from datetime import date

class Firm(models.Model):
    name = models.CharField(max_length=128, verbose_name=_("firm name"))
    address = models.TextField(verbose_name=_('address'))
    inn = models.CharField(max_length=12, verbose_name=_('INN'))
    bank = models.TextField(verbose_name=_("bank full name"))
    racc = models.CharField(max_length=24, verbose_name=_('racc'))
    cacc = models.CharField(max_length=24, verbose_name=_('cacc'))
    bic = models.CharField(max_length=24, verbose_name=_('bic'))
    boss_name = models.CharField(max_length="128", verbose_name=_('boss name'))
    for_print = models.BooleanField(verbose_name=_('use for print'), default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('firm')
        verbose_name_plural = _('firms')

class Commission(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('Commissioner name'))
    post = models.CharField(max_length=64, verbose_name=_('post'))
    order = models.IntegerField(verbose_name=_('Order in list'))

    def __unicode__(self):
        return _('Commission #%s') % self.pk

    class Meta:
        verbose_name = _('Commission member')
        verbose_name_plural = _('Commission members')

class Task(models.Model):
    STATUSES = (
        ('new', 'Новая'),
        ('expertise', 'Экспертиза'),
        ('write-off', 'Списание'),
        ('ended', 'Закрыта')
    )
    
    date_in = models.DateField(auto_now_add=True)
    date_out = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUSES, default='new')
    doc_url = models.CharField(max_length=128, null=True, blank=True)

    def __unicode__(self):
        return "Task #%s" % self.pk

    def close(self):
        self.status = 'ended'
        self.date_out = date.today()
        self.save()

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
        ordering = ['id']

class Request(models.Model):
    user = models.ForeignKey(Employee)
    task = models.ForeignKey(Task, blank=True, null=True)
    device = models.CharField(max_length=128, verbose_name=_('device'))
    number = models.CharField(max_length=12, verbose_name=_('inventory number'))
    serial = models.CharField(max_length=24, verbose_name=_('serial number'))
    year = models.CharField(max_length=4, verbose_name=_('year'))
    doc_url = models.CharField(max_length=128, verbose_name=_('url to generated document'), default='')
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "Request #%s (%s)" % (self.pk, self.device)

    def get_status(self):
        if self.deleted:
            return u'Отклонена'
        if not self.task:
            return u'Новая'
        else:
            if self.task.status == 'new':
                return u'В работе'
        return self.task.get_status_display()

    class Meta:
        verbose_name = _('request')
        verbose_name_plural = _('requests')
        ordering = ['id']

class Comment(models.Model):
    request = models.ForeignKey(Request)
    comment = models.TextField()
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Employee)

    def __unicode__(self):
        return 'Comment for request #%s' % self.request.pk

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['time']

