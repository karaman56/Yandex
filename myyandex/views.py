from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Place, Image
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
            "detailsUrl": f"/places/{place.id}/"
          }
        }
        geojson["features"].append(feature)

    places_json = json.dumps(geojson, ensure_ascii=False, indent=2)
    return render(request, 'myyandex/index.html', {'places_json': places_json})


def place_json(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    images = place.images.order_by('position')
    return JsonResponse({
      'title': place.title,
      'imgs': [request.build_absolute_uri(image.image.url) for image in images],
      'description_short': place.description_short,
      'description_long': place.description_long,
      'coordinates': {
        'lng': place.lng,
        'lat': place.lat,
      }
    }, json_dumps_params={'ensure_ascii': False, 'indent': 2})


def place_details(request):
    place_id = request.GET.get('place_id')
    if not place_id:
        return JsonResponse({'error': 'Missing place_id parameter'}, status=400)
    try:
        return place_json(request, int(place_id))
    except ValueError:
        return JsonResponse({'error': 'Invalid place_id format'}, status=400)





