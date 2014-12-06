from django import forms
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory, inlineformset_factory

from profiles.models import GiftGroup, Invitation

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            'username': 'Name',
            }


class InviteForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ('to_name', 'to_email')
        labels = {
            'to_name': 'Name',
            'to_email': 'Email',
            }

InviteFormSet = modelformset_factory(
    model = Invitation,
    form=InviteForm,
    fields = ('to_name', 'to_email'),
    extra=5)

