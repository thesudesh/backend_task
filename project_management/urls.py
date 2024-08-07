from django.urls import path,include
from project_management import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

router=DefaultRouter()
router.register(r'users', views.Userview)

# router.register(r'department', views.DepartmentView.as_view())
# router.register(r'department/<int:id>', views.DepartmentView.as_view())
# router.register(r'project', views.ProjectView.as_view())



urlpatterns = [
    path('exportapi/', views.export_csv),
    path('projectapi/',views.ProjectView),
    path('projectapi/<int:id>/',views.ProjectView),
    path('departmentapi/', views.DepartmentView.as_view()),
    path('departmentapi/<int:id>',views.DepartmentView.as_view()),
    path('documentapi/',views.DocumentView.as_view()),
    path('documentapi/<int:id>',views.Documentedit.as_view()),
    path('', include(router.urls))
]
