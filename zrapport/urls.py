from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('zrapport.views',
	url(r'^counting/(?P<report_type_id>\d+)/$', 'counting'),
	url(r'^new/$', 'new'),
	url(r'^(?P<report_id>\d+)/result/$', 'result'),
	url(r'^(?P<report_id>\d+)/start/$', 'start'),
	url(r'^(?P<report_id>\d+)/settle/$', 'settle'),
	url(r'^(?P<report_id>\d+)/$', 'report'),
	url(r'^unfinished/$', 'unfinished'),
	url(r'^$', 'index'),
)
