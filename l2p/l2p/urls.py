from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'l2p.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    #url(r'^date/', 'l2p.views.date', name='date')

    # Include Zurb Foundation test pages
    url(r'zurb/', include('foundation.urls'))
)
