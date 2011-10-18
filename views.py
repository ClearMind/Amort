# -*- coding: utf-8 -*-
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.template.context import Context
from django.utils.translation import ugettext_lazy as _
from account.models import Employee
from amortization import settings
from models import MenuItem
from task.forms import RequestForm
from task.models import Request

__author__ = 'cm'

from django.template.loader import get_template

def base_context(request):
    author = settings.ADMINS[0][0]
    version = settings.VERSION
    csrf_token = get_token(request)
    media_url = settings.MEDIA_URL
    app_name = _('Amortization & Expertise')
    path = request.path

    logout = False
    if request.user.is_authenticated():
        logout = True

    menu = MenuItem.objects.order_by("order");

    return locals()

def main(request):
    c = base_context(request)
    template = get_template("index.html")
    c['title'] = _('Request')
    form = RequestForm()

    # if user is authenticated
    user = request.user
    c['user'] = user
    if user.is_authenticated():
        e = Employee.objects.filter(user=user)
        if e:
            empl = e[0]
            form = RequestForm(initial={'fio': empl.fio, 'tab_number': empl.tab_number, 'post': empl.post, 'cabinet': empl.cabinet})
            c['logout'] = True

    c['form'] = form

    if request.method == 'POST':
        postdata = request.POST.copy()
        form = RequestForm(request.POST)
        if form.is_valid():
            empl = Employee.objects.filter(tab_number = postdata.get('tab_number', 0))
            if not empl:
                # django user ---
                if user.is_authenticated():
                    # logout
                    logout(request)
                new_user = User()
                new_user.username = postdata.get('fio', 'error!')
                new_user.set_password(postdata.get('tab_number', 0))
                new_user.save()
                # login
                login(request, new_user)

                # amortization user
                empl = Employee()
                empl.tab_number = postdata.get('tab_number', 0)
                empl.fio = postdata.get('fio', "error!")
                empl.user = new_user
                empl.post = postdata.get('post', '')
                empl.cabinet = postdata.get('cabinet', '0-000')
                empl.save()
                uid = empl
            else:
                uid = empl[0]
                login(request, uid.user)

            req = Request()
            req.user = uid
            req.number = postdata.get('number', '000000000000')
            req.device = postdata.get('device', 'NoName')
            req.serial = postdata.get('serial', '')
            req.year = postdata.get('year', '----')
            req.save()
            c['saved'] = True

        else:
            c['form'] = form

    return HttpResponse(template.render(Context(c)))
  