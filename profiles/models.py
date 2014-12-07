from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse

from profiles.slugify import unique_slugify


class Profile(models.Model):
    user = models.OneToOneField(User)
    slug = models.SlugField(unique=True)

    # TODO This is not ideal
    # Doesn't represent the relationship well (asymmetrical)
    partner = models.OneToOneField('Invitation',
                                   related_name='partner_of',
                                   blank=True,
                                   null=True)

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
                                     null=True,
                                     through='Membership',
                                     through_fields=('giftgroup', 'profile'))
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(GiftGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Invitation(models.Model):
    to_name = models.CharField(max_length=50)
    to_email = models.EmailField()
    sender = models.ForeignKey(User)
    key = models.CharField(max_length=20)
    gift_group = models.ForeignKey(GiftGroup)

    def __str__(self):
        return self.to_name

    def send(self):
        subject = '{} has invited you to join a Secret Santa group on ChrApp'.format(
            self.sender.username)
        # link = 'test'
        link = reverse('accept', args=[self.key])
        template = get_template('registration/invitation_email.txt')
        context = Context({
            'to_name': self.to_name,
            'link': link,
            'sender': self.sender.username,
            'group': self.gift_group.name,
            })
        message = template.render(context)
        send_mail(
                subject,
                message,
                self.sender.email,
                [self.to_email]
                )


class Membership(models.Model):
    profile = models.ForeignKey(Profile)
    giftgroup = models.ForeignKey(GiftGroup)

    admin = models.BooleanField(default=False)
    wishlist = models.TextField(blank=True)

    avoid = models.ManyToManyField(Invitation,
                                   symmetrical=False,
                                   related_name='avoided_by',
                                   blank=True,
                                   null=True,
                                   help_text="You may still be assigned one of these people.")

    prefer = models.ManyToManyField(Invitation,
                                    symmetrical=False,
                                    related_name='prefered_by',
                                    blank=True,
                                    null=True,
                                    help_text="You may still not be assigned any of these people.")

    avoid_partner = models.BooleanField(default=False,
                                        help_text="If you check this box, you will definitely not be assigned your partner.")

    recipient = models.OneToOneField(Profile,
                                     related_name='santa',
                                     blank=True,
                                     null=True)

    def __str__(self):
        return self.profile.user.username + 's membership in ' + self.giftgroup.name
