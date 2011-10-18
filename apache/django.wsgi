import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'amortization.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = '/home/cm/dev/django'
if path not in sys.path:
    sys.path.append(path)
    
