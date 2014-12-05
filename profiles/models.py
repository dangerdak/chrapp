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
                                   null=True,
                                   help_text="You may still be assigned one of these people.")

    prefer = models.ManyToManyField('self',
                                    symmetrical=False,
                                    related_name='prefered_by',
                                    blank=True,
                                    null=True,
                                    help_text="You may still not be assigned any of these people.")

    # TODO This is not ideal
    # Doesn't represent the relationship well (asymmetrical)
    partner = models.OneToOneField('self',
                                   related_name='partner_of',
                                   blank=True,
                                   null=True)
    avoid_partner = models.BooleanField(default=False,
                                        help_text="If you check this box, you will definitely not be assigned your partner.")

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


class GiftGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Profile,
                                     blank=True,
                                     null=True)
