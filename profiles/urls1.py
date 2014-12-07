from django.conf.urls import patterns, url  

from profiles.views import ProfileUpdateView, ProfileDetailView

urlpatterns = patterns('',
    url(r'^$',
        ProfileDetailView.as_view(),
        name='profile-detail'),
    url(r'^update/$',
        ProfileUpdateView.as_view(),
        name='profile-update'),
)
