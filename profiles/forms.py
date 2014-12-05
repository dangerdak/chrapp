from django import forms
from django.core.mail import send_mail
from django.forms.models import inlineformset_factory

from registration.models import Invitation
from profiles.models import Profile, GiftGroup


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ()


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self, from_email, to_email):
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        send_mail(subject, message, from_email, [to_email])


class GroupForm(forms.ModelForm):
    class Meta:
        model = GiftGroup
        fields = ['name']

InvitationFormSet = inlineformset_factory(
    GiftGroup, Invitation, fields=['to_name', 'to_email'])
