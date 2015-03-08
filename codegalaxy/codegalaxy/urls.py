from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = patterns('codegalaxy.views',

   ## HOME ##
   # Home page (/)
   url(r'^$', 'home'),

   ## USERS ##
   # User page (/u/<id>)
   url(r'^u/(?P<id>\d*)/$', 'user'),
   # User overview (/u/overview)
   url(r'^u/overview/$', 'userOverview'),
   # Login page (/login)
   url(r'^login', 'login'),
   # Logout page (/logout)
   url(r'^logout', 'logout'),
   # Redirect to user page (/me)
   url(r'^me', 'me'),
   # Register (/register)
   url(r'^register', 'register'),
   # Email verification
   url(r'^verification/(?P<hash_seq>[a-zA-Z0-9_]{32})$', 'verify'),

   ## GROUPS ##
   # Group page (/g/<id>)
   url(r'^g/(?P<id>\d*)/$', 'group'),
   # Group overview (/g/overview)
   url(r'^g/overview/$', 'groupOverview'),
   # Create new group (/g/create)
   url(r'^g/create', 'groupCreate'),

   ## TESTING ##
   # Zurb Foundation test pages
   url(r'zurb/', include('foundation.urls')),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^test', 'test'),
   url(r'^tables/', 'tables'),
   url(r'^python$', 'python'),
   url(r'^graphs', 'graphs')
)

urlpatterns += patterns('codegalaxy.exercises.views',
    url(r'^l/create$', 'createExerciseList'),
    ## QUESTIONS ##
    # List page with overview of questions (/l/<id>)
    url(r'^l/(?P<id>\d*)/$', 'list'),

    # Create exercise for list
    url(r'^l/(?P<listId>\d*)/createExercise/$', 'createExercise'),

    # Question page (/l/<id>/<question>)
    url(r'^l/(?P<list_id>\d+)/(?P<question_id>\d+)$', 'answerQuestion'),
    # Submit question answer (/l/<id>/<question>/submit)
    url(r'^l/(?P<list_id>\d+)/(?P<question_id>\d+)/submit$', 'submit'),
)
