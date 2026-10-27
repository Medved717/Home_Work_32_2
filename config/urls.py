from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("educations/", include("educations.urls", namespace="educations")),
    path("users/", include("users.urls", namespace="urls")),
]
