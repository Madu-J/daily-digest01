from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

# To create a profile picture
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# To save profile picture
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.UserProfile.save()
    