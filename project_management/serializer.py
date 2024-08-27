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
        fields = ['id','name','department','status','team', 'deadline']

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
        # fields= ["project","name","department"]
        
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        datas["project"]= instance.project.name
       
        return datas
                 
# rtmentSerializer(read_only=True)
    
class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model= Summary
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    userprofile = UserSerializer(read_only=True)
    depart = DepartmentSerializer(read_only=True)
    
    class Meta:
        model= Profile
        fields= '__all__'

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data["project"] = instance.project.name
        data["department"] = instance.department.name

        return data


class ProjectSiteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSite
        fields = ['creator','proj_site_cordinates', 'area', 'way_from_home'] 
