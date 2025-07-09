from django.shortcuts import render
from django.http import JsonResponse  # Добавьте этот импорт
import json
import os
from django.conf import settings


def index(request):
  return render(request, 'myyandex/index.html')

def place_details(request):
  place_id = request.GET.get('place_id')
  path = f"myyandex/static/myyandex/places/{place_id}.json"
  return JsonResponse(json.load(open(path, 'r', encoding='utf-8')))

