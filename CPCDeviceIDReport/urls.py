from django.conf.urls import patterns, url
from CPCDeviceIDReport import views

urlpatterns = patterns('',
    url(r'^$', views.query_form, name='index'),
    url(r'^(?P<queryID>[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12})/$', views.query),
)
