import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '../project_management_system.settings')
django.setup()

from django.contrib.auth.models import User
from project_management.models import Project, Department
from django.utils import timezone
import random
from faker import Faker

fake = Faker()

# Function to create departments
def create_departments(num_departments=10):
    departments = []
    for _ in range(num_departments):
        department = Department(
            name=fake.company()
        )
        departments.append(department)
    
    Department.objects.bulk_create(departments)
    print(f"Created {num_departments} departments.")
    return Department.objects.all()

# Function to create users
def create_users(num_users=50):
    users = []
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        users.append(user)
    
    User.objects.bulk_create(users)
    print(f"Created {num_users} users.")
    return User.objects.all()

# Function to create projects
def create_projects(num_projects=100000, departments=None, users=None):
    if departments is None or users is None:
        raise ValueError("Departments and users must be provided.")

    projects = []
    for i in range(num_projects):
        project = Project(
            name=fake.bs().capitalize(),
            department=random.choice(departments),
            deadline=fake.date_between(start_date='today', end_date='+1y'),
            status=random.choice([Project.ACTIVE, Project.CANCELED, Project.COMPLETED, Project.ON_HOLD]),
            manpower=random.randint(1, 100)
        )
        projects.append(project)
    
    Project.objects.bulk_create(projects, batch_size=100000)
    
    # Add users to the projects
    for project in Project.objects.all():
        project.team.add(*random.sample(list(users), min(5, len(users))))

    print(f"Created {num_projects} projects.")

# Main script execution
departments = create_departments()
users = create_users()
create_projects(departments=departments, users=users)
