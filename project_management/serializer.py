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
    # dep = DepartmentSerializer(many=True)
    class Meta:
        model = Project
        fields = '__all__'
        # fields = ["id","user","department"]

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        datas["department"]= instance.department.name
        datas["user"]= instance.user.username
        # breakpoint()
        return datas

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Document
        fields= '__all__'

class ExportSerializer(serializers.ModelSerializer):
    model= Export
    document = serializers.FileField(
        label="Export to CSV"
    )




class UserDetails(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'
        # fields = ["id","user","department"]

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        datas["department"]= instance.department.name
        datas["user"]= instance.user.username
        # breakpoint()
        return datas