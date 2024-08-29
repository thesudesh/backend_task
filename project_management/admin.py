from collections.abc import Callable
from typing import Any
from django.contrib import admin
from project_management.models import *
from import_export.admin import ExportActionMixin
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.

class ProjectDetails(ExportActionMixin,admin.ModelAdmin):
    list_display=["name","department","status", "deadline", "manpower"]
    list_filter=["deadline"]
admin.site.register(Project, ProjectDetails)

class DepartmentDetails(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Department,DepartmentDetails)

class DocumentDetails(admin.ModelAdmin):
    list_display = ['name','project']
    list_filter=["project"]
admin.site.register(Document, DocumentDetails)

class ProfileDetails(OSMGeoAdmin):
    list_display= ['user','username','country','phone']
admin.site.register(Profile,ProfileDetails )

class SummaryDetails(admin.ModelAdmin):
    # list_display = ['user','monthly_total_projects','monthly_total_users','annual_total_projects','annual_total_users','created_at','updated_at']
    list_display = ['monthly_total_projects','monthly_total_users','annual_total_projects','annual_total_users','created_at','updated_at']
admin.site.register(Summary,SummaryDetails)

# @admin.register(Profile)
# class ProfileAdmin(OSMGeoAdmin):
#     list_display = ('user', 'home_address')

# @admin.register(ProjectSite)
class ProjectSiteAdmin(OSMGeoAdmin):
    # list_display = ('project_name', 'creator', 'site_location', 'site_area', 'path_to_site')
    list_display = ['project_name','creator']
admin.site.register(ProjectSite,ProjectSiteAdmin)


admin.site.register(Country)


from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
# from django.contrib.auth.tokens

admin.site.unregister(User)
# admin.site.unregister(Token)
# admin.site.unregister(Group)



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['username'].disabled = True

        return form    
