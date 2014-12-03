from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from profiles.views import ProfileUpdateView


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

    url(r'^invite/$',
        'registration.views.invite',
        name='invite'),

    url(r'^accept/(\w+)/$',
        'registration.views.accept',
        name='accept'),

    url(r'^admin/',
        include(admin.site.urls)),

    # Send email
    url(r'^send-update-email/$',
        'profiles.views.send_update_email',
        name='send-update-email'),

    # Update view
    url(r'^updateprofile/$',
        ProfileUpdateView.as_view(),
        name='update-profile'),

)
