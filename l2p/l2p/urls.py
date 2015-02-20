from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = patterns('l2p.views',

    ## HOME ##
    # Home page (/)
    url(r'^$', 'home'),

    ## USERS ##
    # User page (/u/<id>)
    url(r'^u/(?P<id>\d*)/$', 'user'),
    # User overview (/u/overview)
    url(r'^u/overview/$', 'userOverview'),

    ## GROUPS ##
    # Group page (/g/<id>)
    url(r'^g/(?P<id>\d*)/$', 'group'),

    ## QUESTIONS ##
    # List page with overview of questions (/l/<id>)
    url(r'^l/(?P<id>\d*)/$', 'list'),


    ## TESTING ##
    url(r'^info/', 'info'),
    # Zurb Foundation test pages
    url(r'zurb/', include('foundation.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
