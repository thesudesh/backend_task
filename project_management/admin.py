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
    list_display = ['monthly_total_projects','monthly_total_users','annual_total_projects','annual_total_users','created_at','updated_at']
admin.site.register(Summary,SummaryDetails)


class ProjectSiteAdmin(OSMGeoAdmin):
    list_display = ['project_name','creator']
admin.site.register(ProjectSite,ProjectSiteAdmin)


admin.site.register(Country)


from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['username'].disabled = True

        return form    

class LocationAdmin(OSMGeoAdmin):
    list_display = ['address','location_request']

admin.site.register(TrackedLocation,LocationAdmin)