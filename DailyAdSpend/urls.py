from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.partnerindex, name='partnerindex'),
    url(r'^china/$', views.chart, name='chart'),
    url(r'^(?P<partner_name>\w+)/$', views.month, name='index'),
    url(r'^(?P<partner_name>\w+)/(?P<month>\d+)/$', views.day, name='month'),
    url(r'^(?P<partner_name>\w+)/(?P<month>\d+)/(?P<day>[^/]+)/$', views.download, name='day'),
)
