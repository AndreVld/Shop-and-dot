from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=False, db_index=True, verbose_name='Подтвердил почту?')
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    email = models.EmailField(unique=True)

    def delete(self, using=None, keep_parents=False):
        self.image.delete(save=False)
        super(AdvUser, self).delete()

