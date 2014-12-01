from django.views.generic import UpdateView, DetailView
from django.core.urlresolvers import reverse

from guardian.mixins import PermissionRequiredMixin

from profiles.models import Profile


class ProfileDetailView(PermissionRequiredMixin, DetailView):
    model = Profile

    permission_required = 'profiles.view_profile'



class ProfileUpdateView(PermissionRequiredMixin, UpdateView):
    model = Profile
    fields = ('wishlist', 'prefer', 'avoid')

    permission_required = 'profiles.change_profile'

    def get_success_url(self):
        url = reverse('profile', kwargs={'slug': self.object.slug})
        return url

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render


def send_update_email(request):
    subject = 'Updated wishlist'
    message = 'Your secrect santa recipient, {}, has update their wishlist. It is now:'.format(request.user.username)
    message += request.user.profile.wishlist
    from_email = request.user.email
    to_email = request.user.profile.santa.user.email
    try:
        send_mail(subject, message, from_email, [to_email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return render(request, reverse('profile', kwargs={'slug': request.user.profile.slug}), {})
