from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^snda$', views.jump_snda, name='jumpsnda'),
                       url(r'^appdrive$', views.jump_appdrive,
                           name='jumpappdrive'),

                       )
