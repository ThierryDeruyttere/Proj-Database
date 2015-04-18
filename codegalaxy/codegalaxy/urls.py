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
    # Social overview (/social)
    url(r'^social/$', 'social'),
    # Create new group (/g/create)
    url(r'^g/create', 'groupCreate'),

    # TRANSLATIONS ##
    (r'^i18n/', include('django.conf.urls.i18n')),

    ## TESTING ##
    # Zurb Foundation test pages
    url(r'zurb/', include('foundation.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tables/', 'tables'),
)

urlpatterns += patterns('codegalaxy.exercises.views',
    ## QUESTIONS ##
    # Lists overview
    url(r'^l/$', 'listOverview'),
    # List page with overview of questions (/l/<id>)
    url(r'^l/(?P<id>\d*)/$', 'list'),
    # Create list (/l/create)
    url(r'^l/create/$', 'createExerciseList'),
    # Create exercise for list
    url(r'^l/(?P<listId>\d*)/createExercise/$', 'createExercise'),

    # Exercise page (/l/<id>/<question>)
    url(r'^l/(?P<list_id>\d+)/(?P<exercise_number>\d+)$', 'answerQuestion'),
    # Submit exercise answer (/l/<id>/<question>/submit)
    url(r'^l/(?P<list_id>\d+)/(?P<exercise_number>\d+)/submit$', 'submit'),

    url(r'^l/(?P<listId>\d*)/(?P<exercise_id>\d*)/(?P<exercise_number>\d*)/editExercise/$', 'editExercise'),

    url(r'^l/(?P<listId>\d*)/importExercise/$', 'importExercise'),
    url(r'^l/(?P<listId>\d*)/editList/$', 'editList'),
    url(r'^addHint/', 'addHint'),
)

urlpatterns += patterns('codegalaxy.evaluation.views',
    # Sandbox page #
    url(r'^sandbox/$', 'sandbox'),
    # Sandbox code evaluation page
    # Only for getting the responde of code evaluation
    url(r'^eval/(?P<lang>[a-z+]*)/$', 'evaluate')
)

urlpatterns += patterns('codegalaxy.search.views',
    # Search page, only for getting search results #
    url(r's/groupOverview/$', 'groupOverview')
)
