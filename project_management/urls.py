from django.urls import path,include,re_path
from project_management import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
router.register(r'users', views.UserView)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', views.SummaryDetails),
    path('userdetails/', views.UserDetails),
    path('exportapi/', views.export_csv),
    
    path('projectapi/',views.ProjectView),
    path('projectapi/<int:id>/',views.ProjectView),

    path('departmentapi/', views.DepartmentView.as_view()),
    path('departmentapi/<int:id>',views.DepartmentView.as_view()),
    
    re_path('^document/$', views.DocumentFilter.as_view()),
    
    path('documentapi/',views.DocumentView.as_view()),
    path('documentapi/<int:id>',views.Documentedit.as_view()),
    
    path('export-shapefile/', views.ExportShapefileView.as_view(), name='export_shapefile'),
    path('task-status/<str:task_id>/', views.TaskStatusView.as_view(), name='task_status'),
    path('download/<str:file_name>/', views.FileDownloadView, name='file-download'),

    path('simple/',views.simple, name = 'simple'),
    path('projectsview/', views.ProjectFilter.as_view(), name='projects_grouped_by_week'),

]
