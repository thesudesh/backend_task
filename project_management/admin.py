from django.contrib import admin
from project_management.models import *
from import_export.admin import ExportActionMixin
# Register your models here.

class ProjectDetails(ExportActionMixin,admin.ModelAdmin):
    list_display=["name","department","status", "deadline", "manpower"]
    list_filter=["manpower"]
admin.site.register(Project, ProjectDetails)

class DepartmentDetails(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Department,DepartmentDetails)

class DocumentDetails(admin.ModelAdmin):
    list_display = ['name','project']
    list_filter=["project"]
admin.site.register(Document, DocumentDetails)

class ProfileDetails(admin.ModelAdmin):
    list_display= ['user','username','address','country','phone']
admin.site.register(Profile,ProfileDetails )

class SummaryDetails(admin.ModelAdmin):
    # list_display = ['user','monthly_total_projects','monthly_total_users','annual_total_projects','annual_total_users','created_at','updated_at']
    list_display = ['monthly_total_projects','monthly_total_users','annual_total_projects','annual_total_users','created_at','updated_at']
admin.site.register(Summary,SummaryDetails)