from django.conf.urls import patterns, url

from profiles.views import GroupCreateView

urlpatterns = patterns('',
    # Group create view
    url(r'new/$',
        GroupCreateView.as_view(),
        name='create-group'),
)
