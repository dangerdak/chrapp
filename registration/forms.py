from django import forms
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

from registration.models import Invitation

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


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
        extra=5)
