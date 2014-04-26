from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^vastTagURI$', views.vastFile, name='vastfile'),


                       )
