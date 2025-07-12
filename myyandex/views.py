from django.http import JsonResponse
from django.shortcuts import render
from places.models import Place, Image
import json


def index(request):
  places = Place.objects.all()
  geojson = {
    "type": "FeatureCollection",
    "features": []
  }

  for place in places:
    feature = {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [place.lng, place.lat]
      },
      "properties": {
        "title": place.title,
        "placeId": place.id,
        "detailsUrl": "/place-details/"
      }
    }
    geojson["features"].append(feature)

  places_json = json.dumps(geojson, ensure_ascii=False, indent=2)
  return render(request, 'myyandex/index.html', {'places_json': places_json})


def place_details(request):
  place_id = request.GET.get('place_id')

  if not place_id:
    return JsonResponse({'error': 'Missing place_id parameter'}, status=400)

  try:
    place_id = int(place_id)
    place = Place.objects.get(id=place_id)
    images = place.images.all().order_by('position')
    place_data = {
      'title': place.title,
      'imgs': [request.build_absolute_uri(image.image.url) for image in images],
      'description_short': place.description_short,
      'description_long': place.description_long,
    }
    return JsonResponse(place_data)
  except (ValueError, TypeError):
    return JsonResponse({'error': 'Invalid place_id format'}, status=400)
  except Place.DoesNotExist:
    return JsonResponse({'error': 'Place not found'}, status=404)

