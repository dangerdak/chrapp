from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from profiles.views import ProfileDetailView, ProfileUpdateView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chrapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',
        TemplateView.as_view(template_name='index.html'),
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

    url(r'^admin/',
        include(admin.site.urls)),

    # Profile view for each user
    url(r'^(?P<slug>\w*)/$',
        ProfileDetailView.as_view(),
        name='profile'),

    # Send email
    url(r'^send-update-email/$',
        'profiles.views.send_update_email',
        name='send-update-email'),


    # Update view
    url(r'^(?P<slug>\w*)/update/$',
        ProfileUpdateView.as_view(),
        name='profile-update'),

    # Alternative profile URLs
    url(r'^profile/',
        include('profiles.urls')),

)
