from rest_framework import serializers
from project_management.models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model= User
        fields= ['id','username','email','date_joined']


class DocumentSerializer(serializers.ModelSerializer):
    # ps = ProjectSerializer(project,context={'key':'Hi!!'}

    class Meta:
        model= Document
        fields = '__all__'
        # fields= ["project","name","path","ps"]


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
         model= Department
         fields= '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True, many=True)

    # document = DocumentSerializer(read_only=True, many=True)
    class Meta:
        model = Project
        fields = '__all__'
        # fields = ['id','name','department']

    # def to_representation(self, instance):
    #     datas = super().to_representation(instance)
    #     datas["department"]= instance.department.name
    #     datas["user"]= instance.user.username
        
    #     # breakpoint()
    #     return datas

# class ExportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= Export
#         fields = '__all__'
#         document = serializers.FileField(
#             label="Export to CSV"
#     )
 

    

class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model= Summary
        # fields=['monthly_total_projects','monthly_total_users','annual_total_projects','annual_total_users','created_at','updated_at']
        fields = '__all__'



class ProfileSerializer(serializers.ModelSerializer):
    userprofile = UserSerializer(read_only=True, many=True)
    project = ProjectSerializer(read_only=True, many= True)
    depart = DepartmentSerializer(read_only=True, many=True)
    
    class Meta:
        model= Profile
        fields= '__all__'