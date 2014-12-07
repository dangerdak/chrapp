from django.core import serializers
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from profiles.models import Profile, Membership


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

    i = 0
    # Matching algorithm
    for member in data:
        member['fields']['recipient'] = keys[i]
        i += 1
    for member in serializers.deserialize('python', data):
        member.save()

    return HttpResponseRedirect(reverse('home'))

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
