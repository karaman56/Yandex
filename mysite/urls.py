from django.contrib import admin
from django.urls import path, include
from myyandex import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('place-details/', views.place_details, name='place_details'),
    #path('', show_mysite),
]
