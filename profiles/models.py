from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)

    wishlist = models.TextField(blank=True)
    avoid = models.OneToOneField(User,
                                 related_name='avoid',
                                 blank=True,
                                 null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        permissions = (('view_profile', 'Can view profile'),)


    def __str__(self):
        return self.user.username
