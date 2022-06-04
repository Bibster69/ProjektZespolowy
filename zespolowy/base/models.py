from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

lvl1 = 10
lvl2 = 20
lvl3 = 50
lvl4 = 100

exp_levels = (
    (lvl1, 'Easy'),
    (lvl2, 'Average'),
    (lvl3, 'Complex'),
    (lvl4, 'BOSS'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    difficulty = models.IntegerField(default=200)
    level = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.level)
"""
def create_Profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("Profile created")

post_save.connect(create_Profile, sender=User)

def update_Profile(sender, instance, created, **kwargs):
    if created == False:
        instance.profile.save()
        print("Profile updated")

post_save.connect(update_Profile, sender=User)
"""

class task(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    complete = models.BooleanField(default=False)
    exp = models.IntegerField(choices=exp_levels, default=lvl1, null=True, blank=True)
    exp_added = models.BooleanField(default=False, null=True, blank=True)
    dateTime_created = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return str(self.title + ' ' + self.description)

    class Meta:
        ordering = ['complete']