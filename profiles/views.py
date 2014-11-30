from django.views.generic import UpdateView, DetailView
from django.core.urlresolvers import reverse

from profiles.models import Profile


class ProfileDetailView(DetailView):
    model = Profile


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ('wishlist', 'avoid')

    def get_success_url(self):
        url = reverse('profile', kwargs={'slug': self.object.slug})
        return url
