from django.urls import path,include,re_path
from project_management import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
router.register(r'users', views.UserView)
# router.register(r'documents', views.DocumentView)

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
]
