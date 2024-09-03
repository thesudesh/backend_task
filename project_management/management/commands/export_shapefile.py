from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource, OGRGeometry, SpatialReference
from django.contrib.gis.gdal.driver import Driver
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.utils import LayerMapping
from project_management.models import FeatureCollection

class Command(BaseCommand):
    help = 'Export FeatureCollection data to a Shapefile.'

    def handle(self, *args, **kwargs):
        shapefile_path = 'output.shp'

        mapping = {
            'name': 'name',
            'uploaded_at': 'uploaded_at',
            'geom': 'POINT',  
        }

        lm = LayerMapping(
            FeatureCollection, shapefile_path, mapping,
            transform=False,  
            encoding='UTF-8',
        )

        lm.save(strict=True, verbose=True)

        self.stdout.write(f'Successfully exported to {shapefile_path}')
