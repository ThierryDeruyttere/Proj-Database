from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'l2p.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),


    # TODO Further templating on the foundations html for more generic code?
    url(r'^$', 'l2p.views.home', name='home'),

    url(r'^info/', 'l2p.views.info', name='info'),

    # Include Zurb Foundation test pages
    url(r'zurb/', include('foundation.urls')),

    #url(r'^polls/', include('polls.urls', namespace="polls"))
)
