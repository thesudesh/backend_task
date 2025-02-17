from project_management.models import Project
from project_management.serializer import *
from rest_framework.response import Response
from project_management.models import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication  
import csv
from django.core.paginator import Paginator

@api_view(['GET','POST','PUT','DELETE'])
def ProjectView(request,id=None):

    if request.method == 'GET':
        if id is not None:
            try:
                queryset = Project.objects.get(id=id)
                serializer = ProjectSerializer(queryset)
                return Response(serializer.data)
            except Project.DoesNotExist:
                return Response({'msg': 'Enter valid id'})

        else:
            queryset = Project.objects.all()

            # Pagination
            paginator = PageNumberPagination()
            paginator.page_size = 20 
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            serializer = ProjectSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer= ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'your data has been updated'})
        return Response({'msg':'error'})

    elif request.method == 'PUT':
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            return Response({'msg': 'Project not found'})

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Your data has been updated'})
        return Response({'msg':'Fail to update data'})

    elif request.method == 'DELETE':
        try:
            project = Project.objects.get(id=id)
            project.delete()
            return Response({'msg': 'Your data has been deleted'})
        except:
            return Response({'msg': 'Project not found'})


class Projectedit(generics.RetrieveUpdateDestroyAPIView):
    queryset= Project.objects.all()
    serializer_class= ProjectSerializer
    lookup_field='id'

    
class DepartmentView(APIView):
    def get(self, request, id=None, format=None):
        if id is not None:
            try:
                department= Department.objects.get(id=id)
                serializer= DepartmentSerializer(department)
                return Response(serializer.data)
            except:
                return Response({'msg':'fail to obtain data'})
        project= Department.objects.all()
        serializer= DepartmentSerializer(project, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        department= request.data
        serializer= DepartmentSerializer(data=department)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Department data has been post'})
        return Response({'msg':'Fail to post the data'})

    def put(self, request, id, format=None):
        try:
            department=Department.objects.get(id=id)
            serializer=DepartmentSerializer(department, data= request.data)
        except:
            return Response({"fail to obtain data"})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Department data has been updated'})
        return Response({'msg':'Department data is fail to update'})

    def delete(self, request, id , format=None):
        try:
            department= Department.objects.get(id=id)
        except:
            return Response({'msg':'fail to obtain data'})
        try:
            department.delete()
            return Response({'msg':'Data has been deleted'})
        except:
            return Response({'msg':'Failed to delete the data'})

class DocumentView(generics.ListCreateAPIView):
    queryset= Document.objects.all()
    serializer_class= DocumentSerializer

class Documentedit(generics.RetrieveUpdateDestroyAPIView):
    queryset= Document.objects.all()
    serializer_class= DocumentSerializer
    lookup_field='id'


class UserView(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class= UserSerializer


from django.http import HttpResponse

@api_view(['GET'])
def export_csv(request):
    data = Project.objects.all()
    opts = data.model._meta

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    writer.writerow(field_names)

    for row in data:
        writer.writerow([getattr(row, field) for field in field_names])

    return response


class ProfileView(generics.ListCreateAPIView):
    serializer_class= ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.all()
        return queryset
    
    def post(self, request, format=None):
        profile= request.data
        serializer= ProfileSerializer(data = profile )
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data has been posted'})
        return Response({'msg':'Fail to post the data'})


from .models import Summary
from django.utils.dateparse import parse_date
from datetime import datetime
from rest_framework import status


@api_view(['GET'])
def SummaryDetails(request):
    min_projects = request.query_params.get('min_projects', None)
    max_projects = request.query_params.get('max_projects', None)
    
    queryset = Summary.objects.all()
    
    if min_projects is not None:
        queryset = queryset.filter(annual_total_projects__gte=min_projects)
    if max_projects is not None:
        queryset = queryset.filter(annual_total_projects__lte=max_projects)
    
    queryset = queryset.order_by('-annual_total_projects')
    
    serializer = SummarySerializer(queryset, many=True)
    return Response(serializer.data)

   
    
class DocumentFilter(generics.ListAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = Document.objects.all()
        department_name = self.request.query_params.get('department_name', None)
        
        if department_name is not None:
            queryset = queryset.filter(project__department__name=department_name)
        
        return queryset


class ProjectSummary(APIView):
    serializer_class= ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all(many = True)



from project_management.tasks import export_shapefile_task

class ExportShapefileView(APIView):
    """
    This class exports all the project sites' geospatial data into a shapefile.
    """
    def get(self, request, *args, **kwargs):

        task = export_shapefile_task.delay()
        return Response({"task_id": task.id}, status=202)


from django.http import JsonResponse
from celery.result import AsyncResult
import os
from django.conf import settings

class TaskStatusView(APIView):
    """
    This view checks the status of the shapefile export task and provides
    a download link if the task is completed successfully.
    """

    def get(self, request, task_id, *args, **kwargs):
        task_result = AsyncResult(task_id)

        if task_result.state == 'PENDING':
            return JsonResponse({"state": task_result.state, "status": "Pending..."})

        elif task_result.state == 'SUCCESS':
            zip_file_path = task_result.result

            download_url = request.build_absolute_uri(
                f'/download/{os.path.basename(zip_file_path)}'
            )
            return JsonResponse({
                "state": task_result.state,
                "status": "Task completed successfully",
                "download_url": download_url
            })

        elif task_result.state == 'FAILURE':
            return JsonResponse({"state": task_result.state, "status": str(task_result.info)})

        else:
            return JsonResponse({"state": task_result.state, "status": task_result.info})


from django.http import Http404

def FileDownloadView(request, file_name):
    """
    Serve the downloaded file.
    """
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        raise Http404("File not found")


from .tasks import simple_task

def simple(request):
    simple_task.delay()
    return HttpResponse("Done")


from django.db.models.functions import TruncWeek
from django.db.models import Count
from collections import defaultdict
import calendar

class ProjectFilter(APIView):
    def get(self, request, *args, **kwargs):
        projects = (
            Project.objects.annotate(week=TruncWeek('start_date'))
            .values('week')
            .annotate(count=Count('id'))
            .order_by('week')
        )

        grouped_projects = defaultdict(int)

        for project in projects:
            week_start = project['week']
            week_number = week_start.strftime('%U')  
            month_name = week_start.strftime('%B')  
            year = week_start.strftime('%Y')  

            week_key = f"{month_name}_week_{int(week_number)}"
            grouped_projects[week_key] += project['count']

        return Response(grouped_projects)


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user), 
            'auth': str(request.auth),  
        }
        return Response(content)
    

from drf_spectacular.utils import extend_schema, OpenApiParameter
from datetime import date



class ProjectFilterView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='from', description='Deadline Date in YYYY-MM-DD format', required=True, type=str),
            OpenApiParameter(name='to', description='Deadline Date in YYYY-MM-DD format', required=True, type=str),
        ]
    )
    def get(self, request):
        from_str = request.query_params.get('from')
        to_str = request.query_params.get('to')

        if not from_str or not to_str:
            return Response({"error": "Both start_date and end_date are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            from_date = date.fromisoformat(from_str)
            to_date = date.fromisoformat(to_str)
        
        except ValueError:
            return Response({"error": "Invalid date format. Please use YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        projects = Project.objects.filter(start_date__gte=from_date, deadline__lte=to_date)
    
        paginator = PageNumberPagination()
        paginator.page_size = 20 
        paginated_queryset = paginator.paginate_queryset(projects, request)
        serializer = ProjectSerializer(paginated_queryset, many=True) 

        return paginator.get_paginated_response(serializer.data)


from django.db.models.functions import ExtractMonth, ExtractDay
from django.db.models import F


class ProjectWeekCountView(APIView):
    def get(self, request):
   
        projects = Project.objects.annotate(day=ExtractDay('start_date'),month=ExtractMonth('start_date'))

        projects = projects.annotate( week_of_month=F('day')/7
        ).values('month', 'week_of_month').annotate(
            project_count=Count('id')
        ).order_by('month', 'week_of_month')

        result = {}

        for project in projects:
            month_name = calendar.month_name[project['month']] 
            week_key = f"{month_name}_Week{project['week_of_month']}"
            result[week_key] = project['project_count']

        return Response(result)

class ProjectSiteView(generics.ListCreateAPIView):
    queryset = ProjectSite.objects.all()
    serializer_class = ProjectSiteListSerializer


class LocationView(generics.CreateAPIView):
    queryset = LocationRequest.objects.all()
    serializer_class = LocationSerializer

class CountryView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

import json
from django.conf import settings
from django.shortcuts import render
from .models import FeatureCollection

def process_geojson_view(request):
    file_path = 'media/document/file.geojson'
    
    try:
        with open(file_path, 'r') as file:
            geojson_data = json.load(file)
        
        for feature in geojson_data.get('features', []):
            properties = feature.get('properties', {})

            attachments = properties.pop('_attachments', [])
            
            simplified_attachments = [
                {
                    'download_url': attachment.get('download_url', ''),
                    'filename': attachment.get('filename', '')
                }
                for attachment in attachments
            ]

            FeatureCollection.objects.create(
                name=properties.get('Name_of_Pregnant_Woman', 'Unknown'),
                geojson_data={
                    'type': 'Feature',
                    'geometry': feature.get('geometry', {}),
                    'properties': {**properties, '_attachments': simplified_attachments}
                }
            )
        
        return HttpResponse('GeoJSON file processed and data saved successfully.')
    
    except FileNotFoundError:
        return HttpResponse('GeoJSON file not found.', status=404)
    except json.JSONDecodeError:
        return HttpResponse('Error decoding GeoJSON file.', status=400)

class FeatureView(generics.ListAPIView):
    def get(self, request, id=None, format=None):
        if id is not None:
            try:
                feature= FeatureCollection.objects.get(id=id)
                serializer= FeatureSerializer(feature)
                return Response(serializer.data)
            except:
                return Response({'msg':'fail to obtain data'})
        feature= FeatureCollection.objects.all()
        serializer= FeatureSerializer(feature, many=True)
        return Response(serializer.data)


# class UploadGeoJSONView(APIView):
#     def post(self, request, *args, **kwargs):
#         geojson_file = request.FILES.get('file')
#         data = json.load(geojson_file)

#         try:      
#             features = data.get('features', [])

#             for feature in features:
#                 properties = feature['properties']
#                 geometry = feature['geometry']
#                 name=properties.get('Name_of_Pregnant_Woman')

#                 if geometry['type'] == 'Point':
#                     coordinates = geometry['coordinates'][:2]  
#                     geom = Point(coordinates[0], coordinates[1], srid=4326)
#                 else:
#                     geom = GEOSGeometry(json.dumps(geometry), srid=4326).clone()

#                 feature_collection = FeatureCollection(
#                     name=name,
#                     geojson_data=properties,
#                     geom=geom
#                 )
#                 feature_collection.save()

#             return Response({"status": "success"}, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from celery.result import AsyncResult
from .tasks import process_geojson_file

class UploadGeoJSONView(APIView):
    def post(self, request, *args, **kwargs):
        geojson_file = request.FILES.get('file')

        if not geojson_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            geojson_data = geojson_file.read().decode('utf-8')

            task = process_geojson_file.delay(geojson_data)

            return Response({
                "status": "File processing started",
                "task_id": task.id  
            }, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from celery.result import AsyncResult

class TaskStatus(APIView):
    def get(self, request, task_id, *args, **kwargs):
        task_result = AsyncResult(task_id)

        if task_result.state == 'PENDING':
            return Response({"status": "Processing"}, status=status.HTTP_200_OK)
        elif task_result.state == 'SUCCESS':
            return Response({"status": "Completed", "result": task_result.result}, status=status.HTTP_200_OK)
        elif task_result.state == 'FAILURE':
            return Response({"status": "Failed", "error": str(task_result.info)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"status": task_result.state}, status=status.HTTP_200_OK)



class DownloadGeoJSONDataView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            feature_collections = FeatureCollection.objects.all()

            features = []
            for feature in feature_collections:
                features.append({
                    "type": "Feature",
                    "geometry": json.loads(feature.geom.geojson),  
                    "properties": feature.geojson_data 
                })

            geojson_data = {
                "type": "FeatureCollection",
                "features": features
            }

            response = HttpResponse(json.dumps(geojson_data), content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="feature_collection.geojson"'
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
