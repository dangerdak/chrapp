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
            if self.request.user.profile.recipient:
                context['recipient'] = self.request.user.profile.recipient
                context['recipient_wishlist'] = self.request.user.profile.recipient.wishlist
                context['recipient_username'] = self.request.user.profile.recipient.user.username
                if self.request.user.profile.recipient.partner:
                    context['recipient_partner'] = self.request.user.profile.recipient.partner
                    context['recipient_partner_username'] = self.request.user.profile.recipient.partner.user.username
                    context['recipient_partner_santa'] = self.request.user.profile.recipient.partner.santa
                elif self.request.user.profile.recipient.partner_of:
                    context['recipient_partner'] = self.request.user.profile.recipient.partner_of
                    context['recipient_partner_username'] = self.request.user.profile.recipient.partner_of.user.username
                    context['recipient_partner_santa'] = self.request.user.profile.recipient.partner_of.santa
        return context


    #def get(self, request):
    #    return render(request, self.template_name, {
    #        'is_admin': request.user.profile.admin,
    #        'username': request.user.username,
    #        'wishlist': request.user.profile.wishlist,
    #        'prefers': request.user.profile.prefer.all,
    #        'avoids': request.user.profile.avoid.all,
    #        'recipient': request.user.profile.recipient,
    #        'recipient_wishlist': request.user.profile.recipient.wishlist,
    #        'recipient_username': request.user.profile.recipient.user.username,
    #        'recipient_partner': request.user.profile.recipient.partner,

    #        })



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
        form.send_email(self.request.user.profile.recipient.user.email)
        return super(ContactView, self).form_valid(form)
