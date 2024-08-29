from django.contrib.auth.models import User
from django.contrib.gis.db import models


# class Departmentmanager(models.Manager):
#     def get_it(self):
#         return self.filter(name="Tech")
#     def get_hr(self):
#         return self. filter(name="HR")


class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, default=None,primary_key=True)
    home_address=models.PointField(srid=4326, blank=True, null=True)
    username= models.CharField( max_length=50, null=True)
    phone= models.CharField(max_length=10, null= True)
    country= models.CharField( max_length=50, null=True)
    
class Department(models.Model):
    name= models.CharField(max_length=50)
    # department_object=Departmentmanager()

    def __str__(self):
        return self.name



from django.utils.translation import gettext_lazy as _
    
class Project(models.Model):
    ACTIVE = "Active"
    CANCELED = "Canceled"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"

    STATUS = [
        ("Active", _("Active")),
        ("Canceled", _("Canceled")),
        ("Completed", _("Completed")),
        ("On Hold", _("On Hold")),
    ]

    team= models.ManyToManyField(User,blank=True)
    name= models.CharField(max_length=50)
    department= models.ForeignKey(Department, on_delete=models.CASCADE, blank=True , null=True)
    start_date = models.DateField()
    deadline = models.DateField(blank = True, null = True)
    status = models.CharField(max_length=10, choices=STATUS, default=ACTIVE, null=True, blank=True)
    manpower = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class Document(models.Model):
    project= models.ForeignKey(Project, related_name="document", on_delete=models.CASCADE)
    name= models.CharField( max_length=50)
    path= models.FileField(upload_to="document/")

    def __str__(self):
        return self.name


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ProjectSite(models.Model):
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True) 
    creator = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True) 
    proj_site_cordinates= models.PointField(srid=4326, blank=True, null=True)
    area= models.PolygonField(srid=4326,blank=True, null=True)
    way_from_home=models.LineStringField(srid=4326,blank=True, null=True)


class Summary(TimeStampMixin,models.Model):
    monthly_total_projects = models.PositiveBigIntegerField(null=True, blank=True)
    monthly_total_users = models.PositiveBigIntegerField(null=True, blank=True)
    annual_total_projects = models.PositiveBigIntegerField(null=True, blank=True)
    annual_total_users = models.PositiveBigIntegerField(null=True, blank=True)
   
class Country(models.Model):
    iso_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)
    geometry = models.MultiPolygonField(srid=4326)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name