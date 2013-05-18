from django.conf.urls import patterns, url

from ElexTech import views

urlpatterns = patterns('',
    url(r'^$', views.month, name='index'),
    url(r'^(?P<month>\d+)/$', views.day, name='month'),
    url(r'^(?P<month>\d+)/(?P<day>[^/]+)/$', views.download, name='day'),
)
