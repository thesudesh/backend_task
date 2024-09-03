import json
from django.core.management.base import BaseCommand
from django.conf import settings
from project_management.models import FeatureCollection

class Command(BaseCommand):
    help = 'Process GeoJSON file and store its data in the database.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the GeoJSON file.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

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

        self.stdout.write(self.style.SUCCESS('GeoJSON file processed and data saved successfully.'))
