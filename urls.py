from django.conf.urls.defaults import *

from django.contrib import admin
from amortization.task.views import *
from amortization.views import main
from amortization.account.views import list_users, user_info
from amortization.account.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', main),
    (r'^user/(\S{3}.*)/$', list_users),
    (r'^user_info/(\S{3}.*)/$', user_info),
    (r'^my_requests/$', user_requests),
    (r'^all_requests/$', requests),
    (r'^closed_requests/$', ended_requests),
    (r'^deleted/$', deleted),
    (r'^delete_request/$', delete_request),
    (r'^all_tasks/$', tasks),
    (r'^closed_tasks/$', closed_tasks),
    (r'^task_status/$', task_status),
    (r'^task/(\d+)/', task),
    (r'^process_requests/$', request_actions),
    (r'^process_tasks/$', tasks_actions),
    (r'^get_url/request/$', get_resultdoc_url),
    (r'^get_url/task/$', get_actdoc_url),
    (r'^user_requests/(\d+)/$', user_requests_admin),
    (r'^comments/(\d+)/$', comments),

    # ACCOUNTS
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),

    # HTML PRINT
    (r'print/task/(\d+)/', print_task),
)
