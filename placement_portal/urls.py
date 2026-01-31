"""URL configuration for Smart College Placement Portal."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from portal import views as portal_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", portal_views.landing, name="landing"),
    path("accounts/", include("accounts.urls")),
    path("student/", include("portal.urls.student_urls")),
    path("recruiter/", include("portal.urls.recruiter_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
