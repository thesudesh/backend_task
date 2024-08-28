from project_management.models import Project
from project_management.serializer import *
from rest_framework.response import Response
from project_management.models import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination

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


    # if request.method == 'GET':
    #     if id is not None:
    #         try:
    #             queryset= Project.objects.get(id=id)
    #             serializer= ProjectSerializer(queryset,many=True)
    #             return Response(serializer.data)
    #         except:
    #             return Response({'msg':'Enter valid id'})
    #     try:
    #         queryset= Project.objects.all()
    #         serializer= ProjectSerializer(queryset,many=True)


    #         return Response(serializer.data)
    #     except Exception as e:
    #         return Response({'msg':str(e)})
        
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

@api_view(['GET'])
def UserDetails(request):
    queryset= Profile.objects.all()
    serializer= ProfileSerializer(queryset, many = True)

    return Response(serializer.data)

from .models import Summary
from django.utils.dateparse import parse_date
from datetime import datetime
from rest_framework import status


@api_view(['GET'])
# @api_view(['GET'])
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


# @api_view(['GET'])
class ProjectSummary(APIView):
    serializer_class= ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all(many = True)


# from rest_framework import generics
# import geopandas as gpd
# from shapely.geometry import Point, LineString, shape
# import json
# import os
# import shutil
# import tempfile
# from project_management.serializer import ProjectSiteListSerializer
# class export_shapefile(generics.ListAPIView):
#     """
#     This class export all the project sites geospatial data into shapefile.
#     """

#     serializer_class = ProjectSiteListSerializer
#     queryset = ProjectSite.objects.all()

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         data_points = []
#         data_areas = []
#         data_ways = []
#         for project_site in queryset:
#             if project_site.proj_site_cordinates:
#                 point_geometry = Point(project_site.proj_site_cordinates)
#                 points = {"geometry": point_geometry}
#                 data_points.append(points)

#             if project_site.area:
#                 area_geometry = shape(json.loads(project_site.area.geojson))
#                 areas = { "geometry": area_geometry}
#                 data_areas.append(areas)

#             if project_site.way_from_home:
#                 way_geometry = LineString(project_site.way_from_home)
#                 ways = { "geometry": way_geometry}
#                 data_ways.append(ways)
#         temp_dir = tempfile.mkdtemp()
#         shapefile_base = "project-site-geodata"
#         shapefile_path_base = os.path.join(temp_dir, shapefile_base)
#         shapefile_name_points = "project-site-points"
#         shapefile_name_areas = "project-site-areas"
#         shapefile_name_ways = "project-site-ways"
#         shapefile_path_points = os.path.join(shapefile_path_base, shapefile_name_points)
#         shapefile_path_areas = os.path.join(shapefile_path_base, shapefile_name_areas)
#         shapefile_path_ways = os.path.join(shapefile_path_base, shapefile_name_ways)
#         try:
#             os.makedirs(shapefile_path_points, exist_ok=True)
#             os.makedirs(shapefile_path_areas, exist_ok=True)
#             os.makedirs(shapefile_path_ways, exist_ok=True)
#         except OSError as e:
#             print(f"Error in creating dirs in temp dirs: {e}")
#         gdf_points = gpd.GeoDataFrame(data_points, geometry="geometry")
#         gdf_points.to_file(shapefile_path_points, driver="ESRI Shapefile")

#         gdf_areas = gpd.GeoDataFrame(data_areas, geometry="geometry")
#         gdf_areas.to_file(shapefile_path_areas, driver="ESRI Shapefile")

#         gdf_ways = gpd.GeoDataFrame(data_ways, geometry="geometry")
#         gdf_ways.to_file(shapefile_path_ways, driver="ESRI Shapefile")

#         shutil.make_archive(shapefile_path_base, "zip", temp_dir, shapefile_base)

#         with open(f"{shapefile_path_base}.zip", "rb") as zip_file:
#             response = HttpResponse(zip_file.read(), content_type="application/zip")
#             response[
#                 "Content-Disposition"
#             ] = f"attachment; filename={shapefile_base}.zip"

#         shutil.rmtree(temp_dir)
#         return response



from project_management.tasks import export_shapefile_task

class ExportShapefileView(APIView):
    """
    This class exports all the project sites' geospatial data into a shapefile.
    """
    def get(self, request, *args, **kwargs):

        task = export_shapefile_task.delay()

        # Returning the task ID
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




# from django.http import FileResponse, Http404

# class FileDownloadView(APIView):
#     """
#     This view serves the downloaded file.
#     """

#     def get(self, request, file_name, *args, **kwargs):
#         file_path = os.path.join(settings.MEDIA_ROOT, file_name)

#         if os.path.exists(file_path):
#             return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
#         else:
#             raise Http404("File not found")




#==================================Purano==================================================#
# import os
# from celery.result import AsyncResult
# from django.http import JsonResponse

# class TaskStatusView(APIView):
#     """
#     This view checks the status of the shapefile export task.
#     """

#     def get(self, request, task_id, *args, **kwargs):
#         task_result = AsyncResult(task_id)

#         if task_result.state == 'PENDING':
#             return JsonResponse({"state": task_result.state, "status": "Pending..."})

#         elif task_result.state == 'SUCCESS':
#             zip_file_path = task_result.result

#             # Send the file as a response
#             with open(zip_file_path, "rb") as zip_file:
#                 response = HttpResponse(zip_file.read(), content_type="application/zip")
#                 response["Content-Disposition"] = f"attachment; filename={os.path.basename(zip_file_path)}"

#             # Clean up: Deleting the zip file after sending it
#             os.remove(zip_file_path)

#             return response

#         elif task_result.state == 'FAILURE':
#             return JsonResponse({"state": task_result.state, "status": str(task_result.info)})

#         else:
#             return JsonResponse({"state": task_result.state, "status": task_result.info})

from .tasks import simple_task

def simple(request):
    simple_task.delay()
    return HttpResponse("Done")


# # @api_view(['GET']):
# class ProjectFilter(APIView):
#     serializer = ProjectSerializer
#     queryset = Project.objects.annotate()


#----------------------------------- Needs to be improved ---------------------------------------#
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

#-----------------Improved One --------------------#

# class ProjectAPI(APIView):

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
    

from drf_spectacular.utils import extend_schema, OpenApiParameter
from datetime import date
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication  



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

        projects = Project.objects.filter(deadline__gte=from_date, deadline__lte=to_date)
    
        paginator = PageNumberPagination()
        paginator.page_size = 20 
        paginated_queryset = paginator.paginate_queryset(projects, request)

        serializer = ProjectSerializer(paginated_queryset, many=True) 
        return paginator.get_paginated_response(serializer.data)
