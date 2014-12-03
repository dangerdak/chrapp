from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from profiles.models import Profile
from profiles.forms import ContactForm


class ProfileUpdateView(UpdateView):
    fields = ('wishlist', 'prefer', 'avoid')

    # Override this so view can be called without object id or slug
    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.profile.id)

    def get_success_url(self):
        url = reverse('home')
        return url


def send_update_email(request):
    """Send updated wishlist from recipient to santa."""
    subject = 'ChrApp: Updated wishlist'
    message = 'Your secrect santa recipient, {}, has update their wishlist. It is now:'.format(request.user.username)
    message += request.user.profile.wishlist
    from_email = request.user.email
    to_email = request.user.profile.santa.user.email
    try:
        send_mail(subject, message, from_email, [to_email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return HttpResponseRedirect(reverse('home'))


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.send_email(self.request.user.profile.recipient.user.email)
        return super(ContactView, self).form_valid(form)
