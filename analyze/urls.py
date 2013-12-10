from django.conf.urls import patterns, url
from mpcd_web.admin import admin_site
from analyze import views

urlpatterns = patterns('',
    # ex: /analyze/
    url(r'^$',  admin_site.admin_view(views.index) , name='index'),
    # ex: /analyze/process/
    url(r'^process/', admin_site.admin_view(views.process), name='process'),
    url(r'^design/', admin_site.admin_view(views.design), name='design'),
    url(r'^plots/', admin_site.admin_view(views.plots),name='plots')
    # # ex: /polls/5/
    # url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)