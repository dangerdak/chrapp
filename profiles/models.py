from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)

    wishlist = models.TextField(blank=True)

    avoid = models.ManyToManyField('self',
                                   symmetrical=False,
                                   related_name='avoided_by',
                                   blank=True,
                                   null=True)

    prefer = models.ManyToManyField('self',
                                    symmetrical=False,
                                    related_name='prefered_by',
                                    blank=True,
                                    null=True)

    recipient = models.OneToOneField('self',
                                     blank=True,
                                     null=True)

    slug = models.SlugField(unique=True)


    class Meta:
        permissions = (('view_profile', 'Can view profile'),)


    def __str__(self):
        return self.user.username
