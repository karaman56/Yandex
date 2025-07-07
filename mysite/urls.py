from django.contrib import admin
from django.urls import path
from myapp.views import show_mysite



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_mysite),
]
