from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from .models import User


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.user_profile.save()
