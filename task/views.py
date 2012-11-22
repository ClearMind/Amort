# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.context import Context
from django.template.loader import get_template
from django.utils.datetime_safe import date
from django.views.decorators.csrf import csrf_exempt
from amortization.account.models import Employee
from amortization.task.models import Request, Task
from amortization.views import base_context
from django.utils.translation import ugettext_lazy as _
from amortization.task.printer import expertise_result, act
from amortization.task.models import Task
from amortization.task.models import Comment

@login_required
def user_requests(request):
    u = request.user
    au = get_object_or_404(Employee, user=u)
    requests = Request.objects.filter(user=au)

    c = base_context(request)
    c['requests'] = requests
    c['user'] = u
    c['title'] = _('Your requests')

    template = get_template("my_requests.html")

    return HttpResponse(template.render(Context(c)))


@login_required
def requests(request):
    u = request.user
    if not u.is_authenticated():
        raise Http404
    if not u.is_staff:
        raise Http404

    requests = Request.objects.filter(task__isnull=True).filter(deleted=False)
    requests_in_tasks = Request.objects.filter(task__isnull=False).exclude(task__status='ended')

    c = base_context(request)
    c['requests'] = requests
    c['requests_in_tasks'] = requests_in_tasks
    c['title'] = _('All requests')

    template = get_template("all_requests.html")

    return HttpResponse(template.render(Context(c)))


@login_required
def ended_requests(request):
    u = request.user
    if not u.is_authenticated():
        raise Http404
    if not u.is_staff:
        raise Http404

    requests_in_tasks = Request.objects.filter(task__status='ended')

    c = base_context(request)
    c['requests'] = requests_in_tasks
    c['title'] = _('All ended requests')

    template = get_template("all_ended_requests.html")

    return HttpResponse(template.render(Context(c)))


@login_required
def deleted(request):
    u = request.user
    if not u.is_authenticated():
        raise Http404
    if not u.is_staff:
        raise Http404

    requests = Request.objects.filter(deleted=True)

    c = base_context(request)
    c['requests'] = requests
    c['title'] = _('Deleted requests')

    template = get_template("deleted_requests.html")

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


@csrf_exempt
def get_actdoc_url(request):
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        task = Task.objects.get(pk=id)
        url = act(task)
        return HttpResponse(url)
    else:
        return HttpResponse("")


def request_actions(request):
    if request.method != 'POST':
        raise Http404
    else:
        postdata = request.POST.copy()
        #        if postdata['action'] == 'delete':
        #            ids = postdata.getlist('request')
        #            if ids:
        #                for i in ids:
        #                    req = Request.objects.filter(pk=i)
        #                    if req:
        #                        req[0].delete()
        #                        # TODO delete document files
        #                return HttpResponseRedirect('/all_requests/')

        if postdata['action'] == 'new_task':
            ids = postdata.getlist('request')
            if ids:
                task = Task()
                task.status = 'new'
                task.save()
                for i in ids:
                    req = Request.objects.filter(pk=i)
                    if req:
                        req[0].task = task
                        req[0].save()
                return HttpResponseRedirect('/all_tasks/')

        if postdata['action'] == 'delete_from_task':
            ids = postdata.getlist('request')
            task = Task.objects.get(pk=postdata['task_id'])
            reqs_count = Request.objects.filter(task=task).count()
            if ids:
                for i in ids:
                    req = Request.objects.filter(pk=i)
                    if req:
                        req[0].task = None
                        req[0].save()
                if len(ids) == reqs_count:
                    task.delete()
                    return HttpResponseRedirect('/all_tasks/')
                return HttpResponseRedirect('/task/%s/' % postdata['task_id'])
        if postdata['action'] == 'undo':
            ids = postdata.getlist('request')
            if ids:
                for i in ids:
                    req = Request.objects.filter(pk=i)
                    if req:
                        req[0].deleted = False
                        req[0].save()
                return HttpResponseRedirect('/all_requests/')


@login_required
def tasks(request):
    u = request.user
    if not u.is_authenticated():
        raise Http404
    if not u.is_staff:
        raise Http404

    c = base_context(request)
    c['tasks'] = Task.objects.exclude(status='ended')
    c['title'] = _('All tasks')

    template = get_template("all_tasks.html")

    return HttpResponse(template.render(Context(c)))


@login_required
def closed_tasks(request):
    u = request.user
    if not u.is_authenticated():
        raise Http404
    if not u.is_staff:
        raise Http404

    c = base_context(request)
    c['tasks'] = Task.objects.filter(status__exact='ended')
    c['title'] = _('Closed tasks')

    template = get_template("all_tasks.html")

    return HttpResponse(template.render(Context(c)))


@login_required
def user_requests_admin(request, uid):
    u = request.user
    if not u.is_authenticated():
        raise Http404
    if not u.is_staff:
        raise Http404

    c = base_context(request)
    template = get_template('user_requests.html')

    user = Employee.objects.get(id=uid)
    requests = Request.objects.filter(user=user).filter(task__isnull=True)
    requests_in_task = Request.objects.filter(user=user).filter(task__isnull=False)
    c['title'] = u'Заявки пользователя'
    c['requests'] = requests
    c['requests_in_tasks'] = requests_in_task
    c['user'] = user

    return HttpResponse(template.render(Context(c)))


@login_required
def task(request, id):
    u = request.user
    if not u.is_authenticated():
        raise Http404
    if not u.is_staff:
        raise Http404

    c = base_context(request)
    task = get_object_or_404(Task, pk=id)
    c['task'] = task
    c['requests'] = Request.objects.filter(task=task)
    c['title'] = _('Task #%s') % id
    template = get_template('task.html')

    return HttpResponse(template.render(Context(c)))


def tasks_actions(request):
    if request.method != 'POST':
        raise Http404
    else:
        postdata = request.POST.copy()
        if postdata['action'] == 'delete':
            ids = postdata.getlist('task')
            if ids:
                for i in ids:
                    task = Task.objects.filter(pk=i)
                    if task:
                        for r in task[0].request_set.all():
                            r.task = None
                            r.save()
                        task[0].delete()
                        # TODO delete document files
                return HttpResponseRedirect('/all_tasks/')


def print_task(request, id):
    task = get_object_or_404(Task, pk=id)
    reqs = task.request_set.all()

    c = base_context(request)
    c['task'] = task
    c['requests'] = reqs

    template = get_template("printer/print_task.html")

    return HttpResponse(template.render(Context(c)))


@csrf_exempt
def task_status(request):
    if request.method != 'POST':
        raise Http404
    else:
        postdata = request.POST.copy()
        id = postdata.get('id', 0)
        value = postdata.get('value', '')
        if not id:
            return HttpResponse("Bad ID")
        if not value:
            return HttpResponse('Bad value')

        task = Task.objects.get(pk=id)
        task.status = value
        if value == 'ended':
            task.date_out = date.today()
        else:
            if task.date_out:
                task.date_out = None
        task.save()

        return HttpResponse('OK')


@csrf_exempt
def delete_request(request):
    if request.method != 'POST':
        raise Http404
    else:
        postdata = request.POST.copy()
        id = postdata.get('id', 0)
        if not id:
            return HttpResponse('Bad ID')

        r = Request.objects.get(pk=id)
        r.deleted = True
        r.save()
        return HttpResponse('OK')


@login_required
def comments(request, rid):
    req = get_object_or_404(Request, pk=rid)
    c = base_context(request)

    if request.method == "POST":
        postdata = request.POST.copy()
        comment = postdata.get('comment', '')
        if comment:
            cm = Comment()
            cm.user = c['employee']
            cm.comment = comment
            cm.request = Request.objects.get(id=rid)
            cm.save()

    comments = req.comment_set.all()
    c['comments'] = comments
    c['title'] = u'Комментарии к заявке'
    c['request'] = req

    template = get_template("comments.html")

    return HttpResponse(template.render(Context(c)))