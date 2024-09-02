from django.db.models.signals import *
from django.dispatch import receiver
from project_management.models import *
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username='sudesh', phone='123456789', country='Nepal')
        print("Profile is created")

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    print("Profile is saved")


from django.contrib.gis.geos import Point
from geopy.geocoders import Nominatim

@receiver(post_save, sender=LocationRequest)
def create_tracked_location(sender, instance, created, **kwargs):
    if created:
        point = Point(instance.longitude, instance.latitude)

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse((instance.latitude, instance.longitude), language='en')

        TrackedLocation.objects.create(
            location_request=instance,
            point=point,
            address=location.address if location else 'Address not found'
        )
