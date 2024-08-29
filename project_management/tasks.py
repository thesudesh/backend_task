import geopandas as gpd
from shapely.geometry import Point, LineString, shape
import json
import os
import shutil
import tempfile
from celery import shared_task
from project_management.models import ProjectSite, Project


@shared_task
def simple_task():
    return "This is a simple test task"



@shared_task(bind=True)
def export_shapefile_task(self):
    queryset = ProjectSite.objects.all()
    data_points = []
    data_areas = []
    data_ways = []

    for project_site in queryset:
        if project_site.proj_site_cordinates:
            point_geometry = Point(project_site.proj_site_cordinates)
            points = {"geometry": point_geometry}
            data_points.append(points)

        if project_site.area:
            area_geometry = shape(json.loads(project_site.area.geojson))
            areas = {"geometry": area_geometry}
            data_areas.append(areas)

        if project_site.way_from_home:
            way_geometry = LineString(project_site.way_from_home)
            ways = {"geometry": way_geometry}
            data_ways.append(ways)

    temp_dir = tempfile.mkdtemp()
    shapefile_base = "project-site-geodata"
    shapefile_path_base = os.path.join(temp_dir, shapefile_base)
    shapefile_name_points = "project-site-points"
    shapefile_name_areas = "project-site-areas"
    shapefile_name_ways = "project-site-ways"
    shapefile_path_points = os.path.join(shapefile_path_base, shapefile_name_points)
    shapefile_path_areas = os.path.join(shapefile_path_base, shapefile_name_areas)
    shapefile_path_ways = os.path.join(shapefile_path_base, shapefile_name_ways)

    try:
        os.makedirs(shapefile_path_points, exist_ok=True)
        os.makedirs(shapefile_path_areas, exist_ok=True)
        os.makedirs(shapefile_path_ways, exist_ok=True)
    except OSError as e:
        return {"error": f"Error in creating dirs in temp dirs: {e}"}

    gdf_points = gpd.GeoDataFrame(data_points, geometry="geometry")
    gdf_points.to_file(shapefile_path_points, driver="ESRI Shapefile")

    gdf_areas = gpd.GeoDataFrame(data_areas, geometry="geometry")
    gdf_areas.to_file(shapefile_path_areas, driver="ESRI Shapefile")

    gdf_ways = gpd.GeoDataFrame(data_ways, geometry="geometry")
    gdf_ways.to_file(shapefile_path_ways, driver="ESRI Shapefile")

    shutil.make_archive(shapefile_path_base, "zip", temp_dir, shapefile_base)

    zip_file_path = f"{shapefile_path_base}.zip"

    return zip_file_path

from django.utils import timezone

@shared_task
def update_project_status():
    today = timezone.now().date()
    
    Project.objects.filter(deadline__gte=today).update(status=Project.ACTIVE)
    Project.objects.filter(deadline__lt=today).update(status=Project.CANCELED)

    return "Project statuses updated."

# @shared_task
# def summary_update():
    