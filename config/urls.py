"""URL configuration for the PumpRun project."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve as static_serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns.append(
        path("media/<path:file_path>", static_serve, {"document_root": settings.MEDIA_ROOT})
    )
