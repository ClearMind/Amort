from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from views import main
from amortization.account.views import list_users, user_info
from amortization.task.views import user_tasks, tasks, get_resultdoc_url
from amortization.account.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', main),
    (r'^user/(\S{3}.*)/$', list_users),
    (r'^user_info/(\S{3}.*)/$', user_info),
    (r'^my_tasks/$', user_tasks),
    (r'^all_tasks/$', tasks),
    (r'^get_url/request/$', get_resultdoc_url),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
)
