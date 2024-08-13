from project_management.models import Project
from project_management.serializer import *
from rest_framework.response import Response
from project_management.models import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
import csv


@api_view(['GET','POST','PUT','DELETE'])
def ProjectView(request,id=None):
    if request.method == 'GET':
        if id is not None:
            try:
                queryset= Project.objects.get(id=id)
                serializer= ProjectSerializer(queryset,many=True)
                return Response(serializer.data)
            except:
                return Response({'msg':'Enter valid id'})
        try:
            queryset= Project.objects.all()
            serializer= ProjectSerializer(queryset,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'msg':str(e)})
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
                department= Department.department_object.get(id=id)
                serializer= DepartmentSerializer(department)
                return Response(serializer.data)
            except:
                return Response({'msg':'fail to obtain data'})
        project= Department.department_object.all()
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
            department=Department.department_object.get(id=id)
            serializer=DepartmentSerializer(department, data= request.data)
        except:
            return Response({"fail to obtain data"})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Department data has been updated'})
        return Response({'msg':'Department data is fail to update'})

    def delete(self, request, id , format=None):
        try:
            department= Department.department_object.get(id=id)
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


# class UserView(APIView):
#     def get(self, request, id=None, format=None):
#         if id is not None:
#             try:
#                 user = User.objects.get(id=id)
#                 serializer = UserSerializer(user)
#                 return Response(serializer.data)
#             except User.DoesNotExist:
#                 return Response({'msg': 'User not found'})
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
    

# class DocumentFilter(generics.ListAPIView):
#     serializer_class= ProjectSerializer
#     def get_queryset(self):
#         user= self.request.user
#         return Project.objects.filter(user=user)

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

    # serializer_class = ExportSerializer(response, many = True)
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
     # Get the optional query parameters if needed (e.g., for filtering further)
    min_projects = request.query_params.get('min_projects', None)
    max_projects = request.query_params.get('max_projects', None)
    
    # Start with all summaries
    queryset = Summary.objects.all()
    
    # Apply filters if provided
    if min_projects is not None:
        queryset = queryset.filter(annual_total_projects__gte=min_projects)
    if max_projects is not None:
        queryset = queryset.filter(annual_total_projects__lte=max_projects)
    
    # Order by annual_total_projects from most to least
    queryset = queryset.order_by('-annual_total_projects')
    
    # Serialize the data
    serializer = SummarySerializer(queryset, many=True)
    return Response(serializer.data)

    # querysets= Summary.objects.all()
    # serailizer= SummarySerializer(querysets, many=True)
    # return Response(serailizer.data)

    
# To filter the document based on the department
class DocumentFilter(generics.ListAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        # Get all Document objects
        queryset = Document.objects.all()
        
        # Get the department name from query parameters
        department_name = self.request.query_params.get('department_name', None)
        
        if department_name is not None:
            # Filter by department name via the related Project
            queryset = queryset.filter(project__department__name=department_name)
        
        return queryset


