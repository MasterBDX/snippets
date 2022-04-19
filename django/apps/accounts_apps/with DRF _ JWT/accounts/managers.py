from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone

from datetime import timedelta

class UserManager(BaseUserManager):

    def create_user(self, phone_number, username, password=None,**extra):
        user = self.model(
            phone_number=phone_number,
            username=username,
            **extra
        )
        user.set_password(password)
        user.email = extra.get("email",None)
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone_number, username, password=None):
        user = self.create_user(
            phone_number, username, password=password, is_staff=True)
        return user

    def create_superuser(self, phone_number, username, password=None, subscribed=True):
        user = self.create_user(phone_number, username, password=password,
                                is_staff=True, is_admin=True,
                                is_validated=True,is_active=True)
        return user





        