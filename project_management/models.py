from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Departmentmanager(models.Manager):
    def get_it(self):
        return self.filter(name="Tech")
    def get_hr(self):
        return self. filter(name="HR")


class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, default=None,primary_key=True)
    address=models.CharField( max_length=50, null=True)
    username= models.CharField( max_length=50, null=True)
    phone= models.CharField(max_length=10, null= True)
    country= models.CharField( max_length=50, null=True)


class Department(models.Model):
    name= models.CharField(max_length=50)
    department_object=Departmentmanager()
    # team= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# class Employee(models.Model):
#     name=models.CharField(max_length=70)
#     address=models.CharField(max_length=90)
#     department=models.ForeignKey(Department, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

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
    start_date = models.DateField(auto_now_add=True)
    deadline = models.DateField(blank = True, null = True)
    status = models.CharField(max_length=10, choices=STATUS, default=ACTIVE, null=True, blank=True)
    manpower = models.IntegerField(blank=True, null=True)
    
    ## Only works for preexisting projects
    # def save(self, *args, **kwargs):
    #     # Set manpower to the count of users in the team
    #     self.manpower = self.team.count()
    #     super().save(*args, **kwargs)
        
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

class Summary(TimeStampMixin,models.Model):
    monthly_total_projects = models.PositiveBigIntegerField(null=True, blank=True)
    monthly_total_users = models.PositiveBigIntegerField(null=True, blank=True)
    annual_total_projects = models.PositiveBigIntegerField(null=True, blank=True)
    annual_total_users = models.PositiveBigIntegerField(null=True, blank=True)
   
