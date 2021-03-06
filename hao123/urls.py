from django.conf.urls import patterns, include, url

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'hao123.views.home', name='home'),
                       # url(r'^hao123/', include('hao123.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)),
                       url(r'^huadmin/', include(admin.site.urls)),
                       url(r'^337/', include('ElexTech.urls')),
                       url(r'^MT/', include('Locojoy.urls', namespace='MT')),
                       url(r'^mac_addr/', include('CPCDeviceIDReport.urls')),
                       url(r'^change_am/', include('ChangeAMSaleRep.urls')),
                       url(r'^adspend/', include('DailyAdSpend.urls')),
                       url(r'^vast/', include('VastVideo.urls')),
                       url(r'^channel/', include('Bridge.urls')),
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                                }),
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.STATIC_ROOT,
                                }),
                            )
