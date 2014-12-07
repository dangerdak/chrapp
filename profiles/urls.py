from django.conf.urls import patterns, url

from profiles.views import (GroupCreateView,
                            GroupListView,
                            GroupUpdateView,
                            GroupDetailView,
                            MembershipDetailView,
                            MembershipListView,
                            MembershipUpdateView)

urlpatterns = patterns('',
    # Group list view
    url(r'^$',
        MembershipListView.as_view(),
        name='membership-list'),

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

#    # Group detail view
#    url(r'^(?P<slug>\w+)/$',
#        GroupDetailView.as_view(),
#        name='group-detail'),

    # Membership detail view
    url(r'^(?P<slug>\w+)/$',
        MembershipDetailView.as_view(),
        name='membership-detail'),

    # Membership update view
    url(r'^(?P<slug>\w+)/updatemembership/$',
        MembershipUpdateView.as_view(),
        name='update-membership'),

    # Assign secret santa pairs
    url(r'^(?P<slug>\w+)/assign/$',
        'pairings.views.assign_pairs',
        name='assign'),

)
