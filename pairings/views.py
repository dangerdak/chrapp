from django.core import serializers
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from profiles.models import Profile, Membership, Invitation

from core.pairings import fill_recipients


def assign_pairs(self, slug):
    members = Membership.objects.filter(giftgroup__slug=slug)
    data = serializers.serialize('python', members)
    # Ensure all recipients set to None
    # to avoid not unique errors when applying matches
    keys = []
    for member in data:
        member['fields']['recipient'] = None
        keys.append(member['fields']['profile'])
    for member in serializers.deserialize('python', data):
        member.save()

    convert(data, invitation_to_profile)

    # Matching algorithm
    fill_recipients(data)

    convert(data, profile_to_invitation)

    for member in serializers.deserialize('python', data):
        member.save()
    return HttpResponseRedirect(reverse('home'))


# TODO this isn't a view...
def convert(data, fcn):
    """Convert data by applying function to all avoids and prefers"""
    # Avoids and prefers are saved as invitations instead of profiles
    # so must be converted before and after assignments are made
    for member in data:
        member['fields']['avoid'] = fcn(member['fields']['avoid'])
        member['fields']['prefer'] = fcn(member['fields']['prefer'])
        if member['fields']['partner']:
            member['fields']['partner'] = fcn(member['fields']['partner'])


def profile_to_invitation(profile_id):
    """Return invitation id corresponding to given profile id."""
    if isinstance(profile_id, list):
        for index, each in enumerate(profile_id):
            profile = Profile.objects.get(id=each)
            invitation = Invitation.objects.get(to_name=profile.user.username)
            profile_id[index] = invitation.id
        return profile_id

    else:
        profile = Profile.objects.get(id=profile_id)
        invitation = Invitation.objects.get(to_name=profile.user.username)
        return invitation.id


def invitation_to_profile(invitation_id):
    """Return profile id corresponding to given invitaion id."""
    if isinstance(invitation_id, list):
        for index, each in enumerate(invitation_id):
            invitation = Invitation.objects.get(id=each)
            profile = Profile.objects.get(user__username=invitation.to_name)
            invitation_id[index] = profile.id
        return invitation_id
    invitation = Invitation.objects.get(id=invitation_id)
    profile = Profile.objects.get(user__username=invitation.to_name)
    return profile.id
