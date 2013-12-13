from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'base.views.home', name='home'),
    url(r'^login$', 'base.views.login', name='login'),
    url(r'^logout$', 'base.views.logout', name='logout'),
    url(r'^register$', 'base.views.register', name='register'),
    url(r'^scheduler/add$', 'scheduler.views.add', name='add'),
    url(r'^scheduler/list$', 'scheduler.views.list', name='list'),
    url(r'^scheduler/show/(?P<id>\d+)/$', 'scheduler.views.show', name='show'),
    url(r'^scheduler/del/(?P<id>\d+)/$', 'scheduler.views.delete', name='delete'),
    url(r'^scheduler/timetable/(?P<task>\d+)/csv/$', 'scheduler.views.timetablecsv', name='timetablecsv'),
    url(r'^scheduler/timetable/(?P<task>\d+)/(?P<curriculum>\w+)/$', 'scheduler.views.timetable', name='timetable'),

    url(r'^scheduler/timetable/(?P<task>\d+)/(?P<curriculum>\w+)/json/$', 'scheduler.views.timetableapi', name='timetableapi'),
    url(r'^accounts/login/$', 'base.views.home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
