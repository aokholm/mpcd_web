from django.conf.urls import patterns, include, url
from mpcd_web.admin import admin_site
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mpcd_web.views.home', name='home'),
    # url(r'^mpcd_web/', include('mpcd_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'myadmin/', include(admin_site.urls)),
)
