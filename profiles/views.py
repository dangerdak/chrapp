from django.views.generic import UpdateView, TemplateView, CreateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

from profiles.models import Profile, GiftGroup, Membership, Invitation
from profiles.forms import ContactForm, GroupForm, InvitationFormSet, MembershipForm, MembershipPairedForm
from profiles.slugify import unique_slugify

class ProfileDetailView(DetailView):
    model = Profile

    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.profile.id)

#class ProfileView(TemplateView):

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
    fields = ['partner']

    # Override this so view can be called without object id or slug
    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.profile.id)

    def get_success_url(self):
        url = reverse('home')
        return url


class MembershipDetailView(DetailView):
    model = Membership

    def get_object(self):
        return get_object_or_404(
            Membership,
            giftgroup__slug=self.kwargs['slug'],
            profile__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(MembershipDetailView, self).get_context_data(**kwargs)
        member = context['membership']
        if member.recipient.partner:
            # TODO what if partner is not in group?
            partner_invite = Invitation.objects.get(id=member.recipient.partner.id)
            partner_profile = Profile.objects.get(user__username=partner_invite.to_name)
            context['recipient_partner_profile'] = partner_profile
            partner_santa_profile = partner_profile.santa_memberships.get(giftgroup=member.giftgroup).profile
            context['recipient_partner_santa_profile'] = partner_santa_profile
        return context

class GroupDetailView(DetailView):
    model = GiftGroup


class MembershipUpdateView(UpdateView):
    model = Membership
   # fields = ('wishlist', 'avoid_partner', 'prefer', 'avoid')

    # Override this so view can be called without object id or slug
    def get_object(self):
        return get_object_or_404(
            Membership,
            giftgroup__slug=self.kwargs['slug'],
            profile__user=self.request.user)
   # def get_object(self):
   #     return get_object_or_404(Profile, pk=self.request.user.profile.id)
    def get_form_class(self):
        if self.object.recipient:
            return MembershipPairedForm
        else:
            return MembershipForm

    def get_success_url(self):
        url = reverse('membership-detail',
                      kwargs={'slug': self.kwargs['slug']})
        return url

def send_update_email(request, to_profile_id, from_member_id):
    """Send updated wishlist from recipient to santa."""
    subject = 'ChrApp: Updated wishlist'
    message = 'Your secrect santa recipient, {}, has update their wishlist. It is now: '.format(request.user.username)
    from_member = Membership.objects.get(id=from_member_id)
    message += from_member.wishlist
    from_email = request.user.email
    to_profile = Profile.objects.get(id=to_profile_id)
    to_email = to_profile.user.email
    try:
        send_mail(subject, message, from_email, [to_email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return HttpResponseRedirect(reverse('membership-detail',
                                        kwargs={'slug': from_member.giftgroup.slug}))


class AnonContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        to_profile_id = self.kwargs['to_profile_id']
        to_email = Profile.objects.get(id=to_profile_id).user.email
        form.send_email('santa', to_email)
        return super(AnonContactView, self).form_valid(form)

    def get_success_url(self):
        # TODO better success_url
        return reverse('home')


class GroupCreateView(CreateView):
    model = GiftGroup
    fields = ['name', 'members']
    form_class = GroupForm
    success_url = reverse_lazy('membership-list')

#     def get(self, request, *args, **kwargs):
#         # TODO what's this for?
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         invitation_form = InvitationFormSet()
#         return self.render_to_response(
#             self.get_context_data(form=form,
#                                   invitation_form=invitation_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        giftgroup = form.save()
        profile = self.request.user.profile
        m = Membership(profile=profile, giftgroup=giftgroup)
        m.admin = True
        m.save()
        self.object = giftgroup
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


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


class MembershipListView(ListView):

    def get_queryset(self):
        return Membership.objects.filter(
            profile__user__username=self.request.user.username)
