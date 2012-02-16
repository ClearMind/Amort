from django.conf.urls.defaults import *

from django.contrib import admin
from views import main
from amortization.account.views import list_users, user_info
from amortization.task.views import user_requests, requests, get_resultdoc_url, request_actions, tasks, tasks_actions, print_task, task, get_actdoc_url
from amortization.account.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', main),
    (r'^user/(\S{3}.*)/$', list_users),
    (r'^user_info/(\S{3}.*)/$', user_info),
# TODO my_requests in menu
    (r'^my_requests/$', user_requests),
    (r'^all_requests/$', requests),
    (r'^all_tasks/$', tasks),
    (r'^task/(\d+)/', task),
    (r'^process_requests/$', request_actions),
    (r'^process_tasks/$', tasks_actions),
    (r'^get_url/request/$', get_resultdoc_url),
    (r'^get_url/task/$', get_actdoc_url),

# ACCOUNTS
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),

# HTML PRINT
    (r'print/task/(\d+)/', print_task),
)
