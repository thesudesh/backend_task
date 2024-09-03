from rest_framework import serializers
from project_management.models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['id','username','email','date_joined']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
         model= Department
         fields= '__all__'


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        # fields = '__all__'
        fields = ['id','name','department','status','team','start_date', 'deadline']

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        datas["department"]= instance.department.name
        datas["team"] = [user.username for user in instance.team.all()]
      
        return datas



class DocumentSerializer(serializers.ModelSerializer):
    ps = ProjectSerializer(read_only=True)
    class Meta:
        model= Document
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model= Country
        fields = '__all__'

    
class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model= Summary
        fields = '__all__'


class ProjectSiteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSite
        fields = ['project_name','creator','proj_site_cordinates', 'area', 'way_from_home']
        
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project_name'] = instance.project_name.name
        data['creator'] = instance.creator.username
        return data

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationRequest
        fields = ['longitude', 'latitude']

class LocDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedLocation
        fields = ['location_request', 'address', 'point']


from django.contrib.gis.geos import Point

class ProfileSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'phone', 'country', 'latitude', 'longitude', 'home_address']

    def create(self, data):
        latitude = data.pop('latitude', None)
        longitude = data.pop('longitude', None)

        if latitude is not None and longitude is not None:
            data['home_address'] = Point(longitude, latitude)

        return Profile.objects.create(**data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.home_address:
            representation['latitude'] = instance.home_address.y
            representation['longitude'] = instance.home_address.x
            
        representation['user'] = instance.user.username

        return representation


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureCollection
        fields = '__all__'