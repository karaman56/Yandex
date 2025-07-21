
import json
import requests
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from places.models import Place, Image
import sys


class Command(BaseCommand):
    help = 'Load places from JSON files'

    def add_arguments(self, parser):
        parser.add_argument('source_dir', type=str, help='Path to directory with JSON files')

    def handle(self, *args, **options):
        source_dir = Path(options['source_dir'])


    if not source_dir.exists():
        self.stdout.write(self.style.ERROR(f"Directory does not exist: {source_dir}"))
        return
    if not source_dir.is_dir():
        self.stdout.write(self.style.ERROR(f"{source_dir} is not a directory"))
        return


    json_files = list(source_dir.glob('*.json'))
    if not json_files:
        self.stdout.write(self.style.WARNING(f"No JSON files found in {source_dir}"))
        return

    self.stdout.write(f"Found {len(json_files)} JSON files")
    for json_path in json_files:
    self.stdout.write(f"\nProcessing: {json_path}")
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                place_data = json.load(f)
                self.stdout.write(f"  Title: {place_data['title']}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  Error loading JSON: {str(e)}"))
            continue
      try:
          place, created = Place.objects.get_or_create(
          title=place_data['title'],
          defaults={
            'description_short': place_data.get('description_short', ''),
            'description_long': place_data.get('description_long', ''),
            'lng': float(place_data['coordinates']['lng']),
            'lat': float(place_data['coordinates']['lat'])
          }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"  Created place: {place.title}"))
        else:
            self.stdout.write(self.style.WARNING(f"  Place already exists: {place.title}"))
      except Exception as e:
          self.stdout.write(self.style.ERROR(f"  Error creating place: {str(e)}"))
          exc_type, exc_obj, exc_tb = sys.exc_info()
          self.stdout.write(self.style.ERROR(f"  Line: {exc_tb.tb_lineno}"))
          continue

      for i, img_url in enumerate(place_data.get('imgs', [])):
        try:
            response = requests.get(img_url)
            response.raise_for_status()
            img_name = img_url.split('/')[-1]
          if not place.images.filter(image__endswith=img_name).exists():
              img = Image(place=place)
              img.image.save(img_name, ContentFile(response.content))
              self.stdout.write(f"    Added image: {img_name}")
          else:
              self.stdout.write(f"    Image already exists: {img_name}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"    Error downloading image: {str(e)}"))

    self.stdout.write(self.style.SUCCESS("\nFinished processing!"))
