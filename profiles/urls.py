from django.conf.urls import patterns, url

from profiles.views import ProfileDetailView, ProfileUpdateView

urlpatterns = patterns('',
    # Profile view
    url(r'(?P<slug>\w*)/$',
        ProfileDetailView.as_view(),
        name='profile'),

    # Update profile
    url(r'(?P<slug>\w*)/update$',
        ProfileUpdateView.as_view(),
        name='profile-update'),
)
