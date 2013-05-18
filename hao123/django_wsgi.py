import os
import django.core.handlers.wsgi
#os.environ['DJANGO_SETTINGS_MODULE'] = 'hao123.settings'
application = django.core.handlers.wsgi.WSGIHandler()
