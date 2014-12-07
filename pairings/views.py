from django.core import serializers
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from profiles.models import Profile, Membership, Invitation


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

    i = 0
    # Matching algorithm
    for member in data:
        member['fields']['recipient'] = keys[i]
        i += 1
    for member in serializers.deserialize('python', data):
        member.save()

    convert(data, profile_to_invitation)
    return HttpResponseRedirect(reverse('home'))

def convert(data, fcn):
    """Convert data by applying function to all avoids and prefers"""
    # Avoids and prefers are saved as invitations instead of profiles
    # so must be converted before and after assignments are made
    for member in data:
        for avoid in member['fields']['avoid']:
            avoid = fcn(avoid)
        for prefer in member['fields']['prefer']:
            prefer = fcn(prefer)
        member.save()

def profile_to_invitation(profile_id):
    """Return invitation id corresponding to given profile id."""
    profile = Profile.objects.get(id=profile_id)
    invitation = Invitation.objects.get(to_name=profile.user.username)
    return invitation.id


def invitation_to_profile(invitation_id):
    """Return profile id corresponding to given invitaion id."""
    invitation = Invitation.objects.get(id=invitation_id)
    profile = Profile.objects.get(user__username=invitation.to_name)
    return profile.id

# def assign_pairs(request):
#     profiles = Profile.objects.all()
#     data = serializers.serialize('python', profiles)
#     # Ensure all recipients set to None
#     # to avoid not unique errors when applying matches
#     for person in data:
#         person['fields']['recipient'] = None
#     for person in serializers.deserialize('python', data):
#         person.save()
# 
#     i = 1
#     # Matching algorithm
#     for person in data:
#         person['fields']['recipient'] = i
#         i += 1
#     for person in serializers.deserialize('python', data):
#         person.save()
# 
#     return HttpResponseRedirect(reverse('home'))
