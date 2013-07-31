from django.conf.urls import patterns, url
from ChangeAMSaleRep import views

urlpatterns = patterns('',
    url(r'^$', views.upload_form),
    url(r'^(?P<queryID>[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12})/$', views.change_result),
)
