from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'base.views.home', name='home'),
    url(r'^scheduler/add$', 'scheduler.views.add', name='add'),
    url(r'^scheduler/list$', 'scheduler.views.list', name='list'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
