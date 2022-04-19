from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractBaseUser):
    phone_number = PhoneNumberField(verbose_name=_('Phone Number'),
                                    max_length=255, unique=True)
    username = models.CharField(_('Username'), max_length=255)
    email = models.CharField(_('Email'), max_length=255, null=True, blank=True)

    slug = models.SlugField(_("Slug"), blank=True, null=True)
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    is_active = models.BooleanField(_("Is Active"), default=False)
    is_staff = models.BooleanField(_("Is Staff"), default=False)
    is_admin = models.BooleanField(_("Is Admin"), default=False)
    is_validated = models.BooleanField(_("Is Validated"), default=False)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_shortname(self):
        return self.username

    def get_fullname(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    def get_absolute_url(self):
        # return reverse('accounts:profile',kwargs={'user_slug':self.slug})
        return reverse('/')


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile',
        verbose_name=_("User"))

    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)

    def __str__(self):
        return self.user + _("Profile")
