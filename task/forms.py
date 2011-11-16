# -*- coding: utf-8 -*-
# from amortization.task.models import Request

__author__ = 'cm'

from django import forms
from django.utils.translation import ugettext_lazy as _

class RequestForm(forms.Form):
    fio = forms.CharField(max_length=32, label=_('FIO'), required=True, help_text=_('Your full name'))
    tab_number = forms.IntegerField(label=_('Tabel number'), required=True, help_text=_('Your tabel number'))
    post = forms.CharField(label=_('Post'), required=True, help_text=_('Your post'))
    cabinet = forms.CharField(label=_('Cabinet'), required=True, help_text=_('Campus and Cabinet in [1-123] format'))
    device = forms.CharField(max_length=128, label=_('Device'), required=True, help_text=_('Device vendor, mark and model'))
    number = forms.CharField(max_length=12, label=_('Inventory number'), help_text=_('Full inventory number [1.1010401234]'), required=True)
    serial = forms.CharField(max_length=24, label=_('Serial number'), help_text=_('Serial number of device'), required=False)
    year = forms.CharField(max_length=4, label=_('Year'), help_text=_('Year when this device bought'), required=True)

    def clean_tab_number(self):
        data = int(self.cleaned_data['tab_number'])
        if data < 1:
            raise forms.ValidationError(_('Tabel number must be grater than 0'))

        return data

    def clean_cabinet(self):
        data = self.cleaned_data['cabinet']

        if len(data) < 5:
            raise forms.ValidationError(_('Campus and cabinet must be in "1-221" format'))