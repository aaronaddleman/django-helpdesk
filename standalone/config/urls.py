from .local_urls import local_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve as serve_media


# django-helpdesk links attachments directly at MEDIA_URL (e.g.
# /media/helpdesk/attachments/...). The usual `static()` helper only serves
# those while DEBUG=True, but this project runs with DEBUG=False, so we serve
# MEDIA_ROOT explicitly. This is handled by Django/Gunicorn, so it works both
# under Docker and on Heroku (no separate web server required).
media_prefix = settings.MEDIA_URL.lstrip("/")

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("helpdesk.urls", namespace="helpdesk")),
        path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    ]
    + [
        re_path(
            rf"^{media_prefix}(?P<path>.*)$",
            serve_media,
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]
    + local_urlpatterns
)
