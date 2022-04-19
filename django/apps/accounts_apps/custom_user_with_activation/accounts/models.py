from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django.template.loader import get_template
from django.core.mail import send_mail
from django.conf import settings

from .managers import UserManager,EmailActivationManager


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',
                              max_length=255, unique=True)
    username = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
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
        return reverse('home')




class EmailActivation(models.Model):
    user = models.ForeignKey('User',
                             related_name='emails_activation',
                             on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120,
                           blank=True,null=True
                           )
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Activation for ' + self.email

    objects = EmailActivationManager()

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False


    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings,'BASE_URL','http://127.0.0.1:8000/')
                activation_url  = reverse('accounts:email_activate',kwargs={'key':self.key})
                context = {
                        'email':self.email,
                        'link':'{}{}'.format(base_url[:-1],activation_url)
                        }
                subject = 'Email Verification'
                message = get_template('accounts/emails/confirmation.txt').render(context)
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                html_message = get_template('accounts/emails/confirmation.html').render(context)
                sent_mail = send_mail(
                        subject, 
                        message,
                        from_email,
                        recipient_list,
                        fail_silently=False,
                        html_message=html_message,
                        )
                return sent_mail

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')

    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user + ' profile'
