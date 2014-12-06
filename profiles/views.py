from django.views.generic import UpdateView, TemplateView, CreateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

from profiles.models import Profile, GiftGroup, Membership
from profiles.forms import ContactForm, GroupForm, InvitationFormSet
from profiles.slugify import unique_slugify


class ProfileView(TemplateView):
    template_name = 'index.html'

#     def get_context_data(self, **kwargs):
#         context = super(ProfileView, self).get_context_data(**kwargs)
#         if self.request.user.is_authenticated():
#             context['username'] = self.request.user.username
#             context['wishlist'] = self.request.user.profile.wishlist
#             context['prefers'] = self.request.user.profile.prefer.all
#             context['avoids'] = self.request.user.profile.avoid.all
#             try:
#                 context['santa'] = self.request.user.profile.santa
#             except ObjectDoesNotExist:
#                 context['santa'] = None
# 
#             if self.request.user.profile.partner:
#                 context['partner'] = self.request.user.profile.partner
#             else:
#                 try:
#                     context['partner'] = self.request.user.profile.partner_of
#                 except ObjectDoesNotExist:
#                     context['partner'] = None
# 
# 
#             if self.request.user.profile.recipient:
#                 recipient = self.request.user.profile.recipient
#                 context['recipient'] = recipient
#                 context['recipient_wishlist'] = recipient.wishlist
#                 context['recipient_username'] = recipient.user.username
# 
#                 if self.request.user.profile.recipient.partner:
#                     partner = self.request.user.profile.recipient.partner
#                     context['recipient_partner'] = partner
#                     context['recipient_partner_username'] = partner.user.username
#                     context['recipient_partner_santa'] = partner.santa
# 
#                 else:
#                     try:
#                         partner = self.request.user.profile.recipient.partner_of
#                         context['recipient_partner'] = partner
#                         context['recipient_partner_username'] = partner.user.username
#                         context['recipient_partner_santa'] = partner.santa
#                     except ObjectDoesNotExist:
#                         context['recipient_partner'] = None
#         return context


class ProfileUpdateView(UpdateView):
    fields = ('wishlist', 'partner', 'avoid_partner', 'prefer', 'avoid')

    # Override this so view can be called without object id or slug
    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.profile.id)

    def get_success_url(self):
        url = reverse('home')
        return url


class MembershipDetailView(DetailView):
    model = Membership


class MembershipUpdateView(UpdateView):
    model = Membership
    fields = ('wishlist', 'avoid_partner', 'prefer', 'avoid')

# If want to show based on who's logged in instead of url
#    # Override this so view can be called without object id or slug
#    def get_object(self):
#        return get_object_or_404(Profile, pk=self.request.user.profile.id)

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


class GroupCreateView(CreateView):
    model = GiftGroup
    fields = ['name', 'members']
    form_class = GroupForm
    success_url = reverse_lazy('home')

#     def get(self, request, *args, **kwargs):
#         # TODO what's this for?
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         invitation_form = InvitationFormSet()
#         return self.render_to_response(
#             self.get_context_data(form=form,
#                                   invitation_form=invitation_form))
# 
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         invitation_form = InvitationFormSet(self.request.POST)
#         if form.is_valid() and invitation_form.is_valid():
#             instances = invitation_form.save(commit=False)
# 
#             for instance in instances:
#                 instance.key = User.objects.make_random_password(20)
#                 instance.sender = request.user
#                 instance.send()
# 
#             unique_slugify(form, form.name)
# 
#             return self.form_valid(form, invitation_form)
#         else:
#             return self.form_invalid(form, invitation_form)
# 
#     def form_valid(self, form, invitation_form):
#         self.object = form.save()
#         invitation_form.instance = self.object
#         invitation_form.save()
#         return HttpResponseRedirect(self.get_success_url())
# 
#     def form_invalid(self, form, invitation_form):
#         return self.render_to_response(
#             self.get_context_data(form=form,
#                                   invitation_form=invitation_form))


class GroupUpdateView(UpdateView):
    model = GiftGroup
    form_class = GroupForm
    fields = ['name', 'members']
    success_url = reverse_lazy('home')


class GroupListView(ListView):
    model = GiftGroup

    def get_queryset(self):
        current_profile = get_object_or_404(
            Profile, user__username__exact=self.request.user.username)
        return current_profile.giftgroup_set.all()
