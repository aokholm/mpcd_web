'''
Created on Dec 15, 2013

@author: aokholmRetina
'''

from django.conf.urls import patterns, url
from mpcd_web.admin import admin_site
from dataimport import views

urlpatterns = patterns('',
    # ex: /analyze/
     url(r'^$',  admin_site.admin_view(views.index) , name='index'),
     url(r'^batch/$', admin_site.admin_view(views.batch) , name='batch'),
     url(r'^batch/thanks/$', admin_site.admin_view(views.thanks), name='thanks')
)