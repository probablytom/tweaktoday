from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('tt_core.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^\'well-known/', include('letsencrypt.urls')),
]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
