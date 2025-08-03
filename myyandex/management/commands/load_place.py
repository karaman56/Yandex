import json
import requests
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from myyandex.models import Place, Image


class Command(BaseCommand):
    help = 'Load places from JSON files'


    def add_arguments(self, parser):
        parser.add_argument('source_dir', type=str, help='Path to directory with JSON files')


    def handle(self, *args, **options):
        source_dir = Path(options['source_dir'])

        if not source_dir.exists():
            raise FileNotFoundError(f"Directory does not exist: {source_dir}")
        if not source_dir.is_dir():
            raise NotADirectoryError(f"{source_dir} is not a directory")

        json_files = list(source_dir.glob('*.json'))
        if not json_files:
            self.stdout.write(self.style.WARNING(f"No JSON files found in {source_dir}"))
            return

        self.stdout.write(f"Found {len(json_files)} JSON files")

        for json_path in json_files:
            self.stdout.write(f"\nProcessing: {json_path}")

            with open(json_path, 'r', encoding='utf-8') as f:
                place_data = json.load(f)

            self.stdout.write(f"  Title: {place_data['title']}")

            place, created = Place.objects.get_or_create(
                title=place_data['title'],
                defaults={
                    'short_description': place_data['description_short'],
                    'long_description': place_data['description_long'],
                    'lng': float(place_data['coordinates']['lng']),
                    'lat': float(place_data['coordinates']['lat']),
                }
            )

            status_style = self.style.SUCCESS if created else self.style.WARNING
            self.stdout.write(status_style(f"  {'Created' if created else 'Found'} place: {place.title}"))

            for i, img_url in enumerate(place_data.get('imgs', [])):
              img_name = img_url.split('/')[-1]

              if place.images.filter(image__endswith=img_name).exists():
                self.stdout.write(f"    Image already exists: {img_name}")
                continue

              response = requests.get(img_url, timeout=10)
              response.raise_for_status()

              Image.objects.create(
                place=place,
                position=i,
                image=ContentFile(response.content, name=img_name)
              )
              self.stdout.write(self.style.SUCCESS(f"    Added image: {img_name}"))

        self.stdout.write(self.style.SUCCESS("\nFinished processing!"))
