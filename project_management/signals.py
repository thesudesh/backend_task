from django.db.models.signals import *
from django.dispatch import receiver
from project_management.models import *
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username='sudesh', phone='123456789', country='Nepal')
        print("Profile is created")

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    print("Profile is saved")