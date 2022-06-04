from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from . import models

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=models.task)
def save_update_task(sender, instance, created, **kwargs):
    if instance.complete == True:
        print("\n\nwywoływanie save_update_task\n\n")
        obj = models.Profile.objects.get(user=instance.user)
        obj.exp_sum += instance.exp
        obj.save()
