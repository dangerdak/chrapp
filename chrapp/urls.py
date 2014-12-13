from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from profiles.views import (ProfileUpdateView,
                            AnonContactView,
                            MembershipListView,
                            GroupCreateView)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chrapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',
        MembershipListView.as_view(),
        name='home'),

    url(r'^register/$',
        'registration.views.register',
        name='register'),

    url(r'^login/$',
        'registration.views.user_login',
        name='login'),

    url(r'^logout/$',
        'registration.views.user_logout',
        name='logout'),

#    url(r'^invite/$',
#        'registration.views.invite',
#        name='invite'),

    url(r'^accept/(\w+)/$',
        'registration.views.accept',
        name='accept'),

    url(r'^admin/',
        include(admin.site.urls)),

    # Update view
    url(r'^updateprofile/$',
        ProfileUpdateView.as_view(),
        name='update-profile'),

    # Send email
    url(r'^update-email/(?P<to_profile_id>\w+)/(?P<from_member_id>\w+)/$',
        'profiles.views.send_update_email',
        name='send-update-email'),

#    # Users
#    url(r'^(?P<username>\w+)/',
#        include('profiles.url')),
#
    # Groups
    url(r'^groups/',
        include('profiles.urls')),

#     # Profiles
#     url(r'^profile/',
#         include('profiles.urls1')),

)
