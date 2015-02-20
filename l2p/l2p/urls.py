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

    # User page (/u/<id>)
    url(r'^u/(?P<id>\d*)/$', 'l2p.views.user'),

    # Group page (/g/<id>)
    url(r'^g/(?P<id>\d*)/$', 'l2p.views.group'),

    # Zurb Foundation test pages
    url(r'zurb/', include('foundation.urls')),

    # TESTING
    url(r'^info/', 'l2p.views.info'),
)
