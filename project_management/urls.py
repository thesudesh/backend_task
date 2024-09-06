from django.urls import path,include,re_path
from project_management import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'users', views.UserView)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', views.SummaryDetails),

    path('profile/', views.ProfileView.as_view()),


    path('exportapi/', views.export_csv),
    
    path('projectapi/',views.ProjectView),
    path('projectapi/<int:id>/',views.ProjectView),

    path('departmentapi/', views.DepartmentView.as_view()),
    path('departmentapi/<int:id>',views.DepartmentView.as_view()),
    
    re_path('^document/$', views.DocumentFilter.as_view()),
    
    path('documentapi/',views.DocumentView.as_view()),
    path('documentapi/<int:id>',views.Documentedit.as_view()),
    
    path('export-shapefile/', views.ExportShapefileView.as_view(), name='export_shapefile'),
    path('status/<str:task_id>/', views.TaskStatusView.as_view(), name='task_status'),
    path('download/<str:file_name>/', views.FileDownloadView, name='file-download'),

    path('simple/',views.simple, name = 'simple'),

    path('geojson/',views.process_geojson_view),
    path('featureview/', views.FeatureView.as_view()),
    path('featureview/<int:id>',views.FeatureView.as_view()),
    path('uploadgeojson/',views.UploadGeoJSONView.as_view()),
    path('task-status/<str:task_id>/', views.TaskStatus.as_view(), name='task_status'),
    path('downloadjson/', views.DownloadGeoJSONDataView.as_view()),


    path('example/', views.ProjectFilterView.as_view()),
    path('projectcount/', views.ProjectWeekCountView.as_view()),
    

    path('tokens/', obtain_auth_token, name='api_token_auth'),

    path('location-request/', views.LocationView.as_view(), name='location-request'),
    path('projectsite/', views.ProjectSiteView.as_view()),

    path('country/', views.CountryView.as_view()),



]
