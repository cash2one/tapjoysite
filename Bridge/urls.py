from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^snda$', views.jump_snda, name='jumpsnda'),
                       url(r'^adwo$', views.jump_adwo, name='jumpadwo'),
                       url(r'^dianxin$', views.jump_dianxin, name='jumpdianxin'),
                       url(r'^appdrive$', views.jump_appdrive,
                           name='jumpappdrive'),
                       url(r'^appdrive_postback$', views.postback_appdrive,
                           name='postbackappdrive'),

                       )
