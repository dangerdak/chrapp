from django import forms
from django.core.mail import send_mail

from profiles.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ()


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self, to_email):
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        # to_email = self.request.user.recipient.user.email
        from_email = 'santa'

        send_mail(subject, message, from_email, [to_email])
