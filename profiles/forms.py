from django import forms
from django.core.mail import send_mail
from django.forms.models import inlineformset_factory

from profiles.models import Profile, GiftGroup, Invitation, Membership

from pagedown.widgets import PagedownWidget


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, required=False)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self, from_email, to_email):
        subject_prefix = '[ChrAppy] '
        subject = subject_prefix + self.cleaned_data['subject']
        message = self.cleaned_data['message']
        message += '\n\n(Please do not reply directly to this email - nobody will read it!)'

        send_mail(subject, message, from_email, [to_email])


class MembershipForm(forms.ModelForm):
    """Membership form for before pairs have been assigned."""
    avoid = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="You may still be assigned a person who you've asked to avoid.")
    prefer = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="You might not be assigned any of the people who you've preferred.")
    partner = forms.ModelChoiceField(queryset=None, required=False)
    wishlist = forms.CharField(widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        # Pop so __init__ doesn't recieve unexpected kwargs
        self.request = kwargs.pop('request')
        self.membership = kwargs.pop('membership')
        super(MembershipForm, self).__init__(*args, **kwargs)
        # Exclude current user from choice field querysets
        # and only include members of current group
        giftgroup = self.membership.giftgroup
        invitations = Invitation.objects.filter(
            gift_group=giftgroup).exclude(to_name=self.request.user.username)
        self.fields['avoid'].queryset = invitations
        self.fields['prefer'].queryset = invitations
        self.fields['partner'].queryset = invitations

    class Meta:
        model = Membership
        fields = ['wishlist', 'partner', 'avoid_partner', 'prefer', 'avoid']


class MembershipPairedForm(forms.ModelForm):
    """Membership form for after pairs have been assigned."""
    wishlist = forms.CharField(widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        # Pop so __init__ doesn't recieve unexpected kwargs
        self.request = kwargs.pop('request')
        self.membership = kwargs.pop('membership')
        super(MembershipPairedForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Membership
        fields = ['wishlist']


class GroupForm(forms.ModelForm):
    class Meta:
        model = GiftGroup
        fields = ['name']

InvitationFormSet = inlineformset_factory(
    GiftGroup, Invitation, fields=['to_name', 'to_email'])
