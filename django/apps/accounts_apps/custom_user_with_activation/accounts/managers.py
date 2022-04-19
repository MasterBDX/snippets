from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone

from datetime import timedelta

class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None,
                    is_active=True, is_staff=False, is_admin=False):
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password=None):
        user = self.create_user(
            email, username, password=password, is_staff=True)
        return user

    def create_superuser(self, email, username, password=None, subscribed=True):
        user = self.create_user(email, username, password=password,
                                is_staff=True, is_admin=True)
        return user


class EmailActivationQueryset(models.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=getattr(settings,'DEFAULT_ACTIVATION_DAYS',2))
        end_range = now
        return self.filter(
                           activated=False,
                           forced_expired=False
                           ).filter(
                               timestamp__gt=start_range,
                               timestamp__lte=end_range
                           )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        queryset = EmailActivationQueryset(self.model,using=self._db)
        return queryset

    def confirmable(self):
        return self.get_queryset()
    
    def email_exists(self,email):
        qs = self.get_queryset().filter(Q(email=email)|
                                          Q(user__email=email)).filter(activated=False)
        return qs
        