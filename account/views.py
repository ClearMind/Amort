# -*- coding: utf-8 -*-
from django.template.context import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt

from amortization.account.models import Employee
from django.contrib.auth.forms import AuthenticationForm
from amortization.views import base_context
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils.simplejson import dumps

@csrf_exempt
def list_users(request, name):
    list = Employee.objects.filter(fio__startswith=name)
    html = "<ul>"
    if list:
        for u in list:
            html += "<li><b>%s</b>%s</li>" % (name, u.fio[len(name):])
    html += '</ul>'

    return HttpResponse(html)

@csrf_exempt
def user_info(request, name):
    list = Employee.objects.filter(fio=name)
    info = {}
    if list:
        empl = list[0]
        info['tab_number'] = empl.tab_number
        info['cabinet'] = empl.cabinet
        info['post'] = empl.post
    return HttpResponse(dumps(info), content_type="text/json")

def login(request):
    c = base_context(request)
    c['title'] = _('Login')
    c['form'] = AuthenticationForm()

    c['next'] = request.GET.get('next', '/my_requests/')

    template = get_template("registration/login.html")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(c['next'])
        else:
            c['form'] = form

    return HttpResponse(template.render(Context(c)))

def logout(request):
    auth_logout(request)

    return HttpResponseRedirect('/')