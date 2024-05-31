from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from users.utils import validate_phone_number


# Create your models here.


class Profile(AbstractUser):
    username = models.CharField(max_length=100, verbose_name=_('username'), unique=True)
    first_name = models.CharField(max_length=100, verbose_name=_('first name'), blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name=_('last name'), blank=True, null=True)
    email = models.EmailField(max_length=254, verbose_name=_('email'), unique=True, null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name=_('address'), blank=True, null=True)
    phone_number = models.CharField(max_length=100, verbose_name=_('phone number'), validators=[validate_phone_number])
    avatar = models.ImageField(upload_to='profile_avatar', verbose_name=_('avatar'), blank=True, null=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username
