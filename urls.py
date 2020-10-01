from django.conf.urls import url
from django.conf.urls import include
from django.shortcuts import redirect
from tastypie.api import Api
from gedgo.api import PersonResource, FamilyResource

from gedgo import views

import settings
import django.contrib.auth.views
import django.views.static

v1_api = Api(api_name='v1')
v1_api.register(PersonResource())
v1_api.register(FamilyResource())

urlpatterns = [
    url(
        r'^(?P<gedcom_id>\d+)/(?P<person_id>I\d+)/$',
        views.person,
        name='person'
    ),
    url(r'^(?P<gedcom_id>\d+)/$', views.gedcom, name='gedcom'),

    # XHR Data views
    url(r'^(?P<gid>\d+)/pedigree/(?P<pid>I\d+)/$', views.pedigree, name='pedigree'),
    url(r'^(?P<gid>\d+)/timeline/(?P<pid>I\d+)/$', views.timeline, name='timeline'),
    url(r'^dashboard/worker/status$', views.worker_status, name='worker_status'),

    url(r'^blog/$', views.blog_list, name='blog'),
    url(r'^blog/(?P<year>\d+)/(?P<month>\d+)/$', views.blog, name='blogmonth'),
    url(r'^blog/post/(?P<post_id>\d+)/$', views.blogpost, name='blogpost'),
    url(r'^documentaries/$', views.documentaries, name='documentaries'),
    url(r'^research/(?P<pathname>.*)$', views.research, name='research'),
    url(r'^api/', include(v1_api.urls), name='api'),
    url(r'^search/$', views.search, name='search'),
    url(r'^list/$', views.people_list, name='people_list'),
    url(r'^list/data/$', views.PeopleListJson.as_view(), name='people_list_json'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/user/(?P<user_id>\d+)/$', views.user_tracking, name='user_tracking'),

    # Auth
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^password_reset/$',
        django.contrib.auth.views.PasswordResetView.as_view(),
        {
            'template_name': 'auth/login.html',
            'email_template_name': 'auth/password_reset_email.html',
            'post_reset_redirect': '/gedgo/password_reset/done/'
        }, name='password_reset'),
    url(r'^password_reset/done/$',
        django.contrib.auth.views.PasswordResetDoneView.as_view(),
        {
            'template_name': 'auth/password_reset_done.html'
        }, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        django.contrib.auth.views.PasswordResetConfirmView.as_view(),
        {
            'post_reset_redirect': '/',
            'template_name': 'auth/password_reset_confirm.html'
        }),
    url(r'^reset/done/', django.contrib.auth.views.PasswordResetCompleteView.as_view(),
        {
            'template_name' : 'auth/password_reset_complete.html'
        }, name='password_reset_complete'),
    url(r'^$', lambda r: redirect('/gedgo/1/')),
]

# Backup media fileserve view
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', django.views.static.serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]


