from django.db import models


class ProfileManager(models.Manager):
    def get_by_natural_key(self, slug):
        print(self.get(slug=slug))
        return self.get(slug=slug)
