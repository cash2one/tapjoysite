import os
import django.core.handlers.wsgi
os.environ['DJANGO_SETTINGS_MODULE'] = 'hao123.settings_production'
application = django.core.handlers.wsgi.WSGIHandler()
