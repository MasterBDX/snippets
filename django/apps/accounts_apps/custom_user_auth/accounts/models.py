from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name=_('Email'),
                              unique=True)
    username = models.CharField(_('Username'), max_length=255)
    slug = models.SlugField(_('Slug'), blank=True, null=True)

    first_name = models.CharField(_('First Name'), max_length=255)
    last_name = models.CharField(_('Last Name'), max_length=255)
    is_active = models.BooleanField(_('IS Active'), default=True)
    is_staff = models.BooleanField(_('IS Staff'), default=False)
    is_admin = models.BooleanField(_('IS Admin'), default=False)

    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username


    def has_perm(self, perm, obj=None):
        '''
            Added this by following the documents
        '''
        return True

    def has_module_perms(self, app_lable):
        '''
            Added this by following the documents
        '''
        return True

