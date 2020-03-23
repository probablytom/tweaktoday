from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('tt_core.urls')),
    path('admin/', admin.site.urls),
]