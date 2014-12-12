import smtplib

from django.views.generic import UpdateView, TemplateView, CreateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib import messages

from profiles.models import Profile, GiftGroup, Membership, Invitation
from profiles.forms import ContactForm, GroupForm, InvitationFormSet, MembershipForm, MembershipPairedForm, ProfileForm
from profiles.slugify import unique_slugify


class ProfileDetailView(DetailView):
    model = Profile

    def get_object(self):
        return get_object_or_404(Profile, pk=self.request.user.profile.id)


class ProfileUpdateView(UpdateView):
    fields = ['partner']
    form_class = ProfileForm

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
        if member.recipient:
            # TODO what if partner is not in group?
            recipient_profile = member.recipient
            recipient_membership = Membership.objects.get(
                profile=recipient_profile, giftgroup=member.giftgroup)
            context['recipient_membership'] = recipient_membership
            context['santa_membership'] = self.request.user.profile.santa_membership

            if recipient_membership.partner:
                recipient_partner_invite = recipient_membership.partner
                recipient_partner_profile = Profile.objects.get(
                    user__username=recipient_partner_invite.to_name)
                context['recipient_partner_profile'] = recipient_partner_profile

                if recipient_partner_profile in member.giftgroup.members.all():
                    recipient_partner_santa_profile = recipient_partner_profile.santa_membership.profile
                    context['recipient_partner_santa_profile'] = recipient_partner_santa_profile
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

    def get_form_kwargs(self):
        kwargs = super(MembershipUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['membership'] = self.object
        return kwargs

    def get_success_url(self):
        url = reverse('membership-detail',
                      kwargs={'slug': self.kwargs['slug']})
        return url

def send_update_email(request, to_profile_id, from_member_id):
    """Send updated wishlist from recipient to santa."""
    subject = '[ChrAppy] Updated wishlist'
    message = 'Your secrect santa recipient, {}, has update their wishlist. It is now: '.format(request.user.username)
    from_member = Membership.objects.get(id=from_member_id)
    message += from_member.wishlist
    # TODO hardcoded domain name
    wishlist_url = 'chrappy.com' + reverse(
        'membership-detail', kwargs={'slug': from_member.giftgroup.slug})
    message += '\n\nView on site: ' + wishlist_url
    message += '\n(Please do not reply directly to this email - nobody will read it!)'
    from_email = request.user.email
    to_profile = Profile.objects.get(id=to_profile_id)
    to_email = to_profile.user.email
    try:
        send_mail(subject, message, from_email, [to_email])
        messages.success(request, "Your wishlist has been sent to Santa. I hope you've been good!")
    except BadHeaderError:
        messages.error(request, 'Invalid header found, email not sent.')
    except smtplib.SMTPException:
        messages.error(request, 'An error occurred, email not sent.')
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

    def get_context_data(self, **kwargs):
        context = super(AnonContactView, self).get_context_data(**kwargs)
        to_profile_id = self.kwargs['to_profile_id']
        to_profile = Profile.objects.get(id=to_profile_id)
        context['to_profile'] = to_profile
        return context

    def get_success_url(self):
        group_slug = self.kwargs['slug']
        return reverse('membership-detail', kwargs={'slug': group_slug})


class GroupCreateView(CreateView):
    model = GiftGroup
    fields = ['name']
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
        # Make group creator member and admin
        m = Membership(profile=profile, giftgroup=giftgroup)
        m.admin = True
        m.save()
        # Also save false invitation for group creator
        i = Invitation(to_name=self.request.user.username,
                       to_email=self.request.user.email,
                       sender=self.request.user,
                       key='fakekey',
                       gift_group=giftgroup)
        i.save()
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
            profile__user__username=self.request.user.username).annotate(
                num_members=Count('giftgroup__members', distinct=True),
                num_invites=Count('giftgroup__invitation', distinct=True))

    def get_context_data(self, **kwargs):
        context = super(MembershipListView, self).get_context_data(**kwargs)
        for member in context['membership_list']:
            membership_count = member.giftgroup.members.count()
            giftgroup = member.giftgroup
            invitation_count = Invitation.objects.filter(gift_group=giftgroup)
        return context
