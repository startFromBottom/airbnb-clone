from django.contrib import admin
from django.urls import path, include  # urls.py -> write in core app
from django.conf import settings  # mirror of settings.py
from django.conf.urls.static import static


urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
