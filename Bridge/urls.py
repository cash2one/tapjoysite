from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^snda$', views.jump_snda, name='jumpsnda'),
                       url(r'^adwo$', views.jump_adwo, name='jumpadwo'),
                       url(r'^dianxin$', views.jump_dianxin, name='jumpdianxin'),
                       )
