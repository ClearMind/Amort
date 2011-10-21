# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.context import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from amortization.account.models import Employee
from amortization.task.models import Request
from amortization.views import base_context
from django.utils.translation import ugettext_lazy as _
from amortization.task.printer import expertise_result

@login_required
def user_tasks(request):
    u = request.user
    au = get_object_or_404(Employee, user = u)
    requests = Request.objects.filter(user=au)

    c = base_context(request)
    c['requests'] = requests
    c['user'] = u
    c['title'] = _('Your requests')

    template = get_template("my_tasks.html")

    return HttpResponse(template.render(Context(c)))

@login_required
def tasks(request):
    u = request.user
    if not u.is_authenticated():
        raise Http404
    if not u.is_staff:
        raise Http404

    requests = Request.objects.all()

    c = base_context(request)
    c['requests'] = requests
    c['title'] = _('All tasks')

    template = get_template("all_tasks.html")

    return HttpResponse(template.render(Context(c)))

@csrf_exempt
def get_resultdoc_url(request):
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        req = Request.objects.get(pk=id)
        url = expertise_result(req)
        return HttpResponse(url)
    else:
        return HttpResponse("")