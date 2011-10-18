# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from amortization.account.models import Employee
from amortization.task.models import Request
from amortization.views import base_context
from django.utils.translation import ugettext_lazy as _
from amortization.models import MenuItem

@login_required
def user_tasks(request):
    u = request.user
    au = Employee.objects.get(user = u)
    requests = Request.objects.filter(user=au)

    c = base_context(request)
    c['requests'] = requests
    c['user'] = u
    c['title'] = _('Your requests')
    c['menu'] = MenuItem.objects.all()

    template = get_template("my_tasks.html")

    return HttpResponse(template.render(Context(c)))
