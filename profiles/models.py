from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    admin = models.BooleanField(default=False,
                                editable=False)
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
                                     related_name='santa',
                                     blank=True,
                                     null=True)

    slug = models.SlugField(unique=True)

    class Meta:
        permissions = (
            ('view_profile', 'Can view profile'),
            ('send_invites', 'Can send invites'),
            ('assign_pairs', 'Can assign Santa-recipient pairs'),
            )

    def __str__(self):
        return self.user.username
