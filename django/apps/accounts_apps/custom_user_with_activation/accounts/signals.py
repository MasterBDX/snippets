from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import User, EmailActivation
from .utils import unique_slug_generator,unique_key_generator


@receiver(pre_save, sender=User)
def get_user_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(post_save, sender=User)
def send_user_email_activation(sender, instance,created, **kwargs):
    if created:
        email_activation_object = EmailActivation.objects.create(user=instance,
                                                          email=instance.email)
        email_activation_object.send_activation()

@receiver(pre_save, sender=EmailActivation)
def get_email_activation_key(sender, instance, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance.__class__)
            