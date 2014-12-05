from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse

from profiles.models import GiftGroup


class Invitation(models.Model):
    to_name = models.CharField(max_length=50)
    to_email = models.EmailField()
    sender = models.ForeignKey(User)
    key = models.CharField(max_length=20)
    gift_group = models.ForeignKey(GiftGroup)

    def __str__(self):
        return 'From {}, to {}'.format(self.sender.username, self.to_email)

    def send(self):
        subject = '{} has invited you join a Secret Santa group on ChrApp'.format(
            self.sender.username)
        # link = 'test'
        link = reverse('accept', args=[self.key])
        template = get_template('registration/invitation_email.txt')
        context = Context({
            'to_name': self.to_name,
            'link': link,
            'sender': self.sender.username,
            })
        message = template.render(context)
        send_mail(
                subject,
                message,
                self.sender.email,
                [self.to_email]
                )
