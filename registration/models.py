from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    wishlist = models.TextField(blank=True)
    avoid = models.OneToOneField(User,
                                 related_name='avoid',
                                 blank=True,
                                 null=True)

    def __str__(self):
        return self.user.first_name
