from django.views.generic import UpdateView, DetailView
from django.core.urlresolvers import reverse

from guardian.mixins import PermissionRequiredMixin

from profiles.models import Profile


class ProfileDetailView(PermissionRequiredMixin, DetailView):
    model = Profile

    permission_required = 'profiles.view_profile'


class ProfileUpdateView(PermissionRequiredMixin, UpdateView):
    model = Profile
    fields = ('wishlist', 'avoid')

    permission_required = 'profiles.change_profile'

    def get_success_url(self):
        url = reverse('profile', kwargs={'slug': self.object.slug})
        return url
