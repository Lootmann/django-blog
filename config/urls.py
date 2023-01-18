from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    # User Management
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
    # pages
    path("", include("pages.urls")),
    # blogs
    path("blogs/", include("blogs.urls")),
]
