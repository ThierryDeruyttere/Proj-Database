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

    # TRANSLATIONS ##
    (r'^i18n/', include('django.conf.urls.i18n')),

    ## TESTING ##
    # Zurb Foundation test pages
    url(r'zurb/', include('foundation.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test', 'test'),
    url(r'^tables/', 'tables'),
    url(r'^python$', 'python'),
    url(r'^graphs', 'graphs'),
    url(r'translation', 'translation')
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
    url(r'^l/(?P<list_id>\d+)/(?P<question_id>\d+)$', 'answerQuestion'),
    # Submit exercise answer (/l/<id>/<question>/submit)
    url(r'^l/(?P<list_id>\d+)/(?P<question_id>\d+)/submit$', 'submit'),

    url(r'^l/(?P<listId>\d*)/(?P<exercise_id>\d*)/(?P<exercise_number>\d*)/editExercise/$', 'editExercise'),

    url(r'^l/(?P<listId>\d*)/importExercise/$', 'importExercise'),

)
