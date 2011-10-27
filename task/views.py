# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.context import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from amortization.account.models import Employee
from amortization.task.models import Request
from amortization.views import base_context
from django.utils.translation import ugettext_lazy as _
from amortization.task.printer import expertise_result
from amortization.task.models import Task

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

def request_actions(request):
    if request.method != 'POST':
        raise Http404
    else:
        postdata = request.POST.copy()
        if postdata['action'] == 'delete':
            ids = postdata.getlist('request')
            if ids:
                for i in ids:
                    req = Request.objects.filter(pk=i)
                    if req:
                        req[0].delete()
                        # TODO delete document files
                return HttpResponseRedirect('/all_tasks/')

        if postdata['action'] == 'new_task':
            ids = postdata.getlist('request')
            if ids:
                task = Task()
                task.status = 'new'
                task.save()
                for i in ids:
                    req = Request.objects.filter(pk=i)
                    if req:
                        req.task = task
                        req.save()
                return HttpResponseRedirect('/all_tasks/')