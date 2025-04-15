# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # o tu modelo de usuario personalizado
from .models import Profile, FounderProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

        if profile.is_founder:
            FounderProfile.objects.create(user=instance, profile=profile)
