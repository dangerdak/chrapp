from django.views.generic import UpdateView, TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from profiles.models import Profile
from profiles.forms import ContactForm


class ProfileView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['is_admin'] = self.request.user.profile.admin
            context['username'] = self.request.user.username
            context['wishlist'] = self.request.user.profile.wishlist
            context['prefers'] = self.request.user.profile.prefer.all
            context['avoids'] = self.request.user.profile.avoid.all
            if self.request.user.profile.partner:
                context['partner'] = self.request.user.profile.partner
            elif self.request.user.profile.partner_of:
                context['partner'] = self.request.user.profile.partner_of

            if self.request.user.profile.recipient:
                recipient = self.request.user.profile.recipient
                context['recipient'] = recipient
                context['recipient_wishlist'] = recipient.wishlist
                context['recipient_username'] = recipient.user.username

                if self.request.user.profile.recipient.partner:
                    partner = self.request.user.profile.recipient.partner
                    context['recipient_partner'] = partner
                    context['recipient_partner_username'] = partner.user.username
                    context['recipient_partner_santa'] = partner.santa

                elif self.request.user.profile.recipient.partner_of:
                    partner = self.request.user.profile.recipient.partner_of
                    context['recipient_partner'] = partner
                    context['recipient_partner_username'] = partner.user.username
                    context['recipient_partner_santa'] = partner.santa
        return context


class ProfileUpdateView(UpdateView):
    fields = ('wishlist', 'partner', 'avoid_partner', 'prefer', 'avoid')

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
        form.send_email('santa', self.request.user.profile.recipient.user.email)
        return super(ContactView, self).form_valid(form)


class ContactPartnerView(FormView):
    template_name = 'contact-partner.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.send_email('santa cousin', self.request.user.profile.recipient.partner.santa.user.email)
        return super(ContactPartnerView, self).form_valid(form)
