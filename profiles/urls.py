from django.conf.urls import patterns, url

from profiles.views import (GroupCreateView,
                            GroupListView,
                            GroupUpdateView,
                            MembershipDetailView,
                            MembershipUpdateView)

urlpatterns = patterns('',
    # Group list view
    url(r'^$',
        GroupListView.as_view(),
        name='group-list'),

    # Group create view
    url(r'^new/$',
        GroupCreateView.as_view(),
        name='create-group'),

    # Group update view
    url(r'^(?P<slug>\w+)/update/$',
        GroupUpdateView.as_view(),
        name='update-group'),

    # Group invite view
    url(r'^(?P<slug>\w+)/invite/$',
        'registration.views.invite',
        name='invite'),

    # Membership detail view
    url(r'^(?P<slug>\w+)/$',
        MembershipDetailView.as_view(),
        name='membership-detail'),

    # Membership update view
    url(r'^(?P<slug>\w+)/updatemembership/$',
        MembershipUpdateView.as_view(),
        name='update-membership'),
)
