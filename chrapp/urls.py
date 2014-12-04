from django.conf.urls import patterns, include, url
from django.contrib import admin

from profiles.views import ProfileUpdateView, ContactView, ContactPartnerView, ProfileView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chrapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',
        ProfileView.as_view(),
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

    url(r'^invite/$',
        'registration.views.invite',
        name='invite'),

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
    url(r'^update-email/$',
        'profiles.views.send_update_email',
        name='send-update-email'),

    # Send anonymous email
    url(r'^anon-email/$',
        ContactView.as_view(),
        name='send-anon-email'),

    # Send anonymous email to recipients partners santa
    url(r'^anon-partner-email/$',
        ContactPartnerView.as_view(),
        name='send-anon-partner-email'),

    # Assign secret santa pairs
    url(r'^assign/$',
        'pairings.views.assign_pairs',
        name='assign'),

)
