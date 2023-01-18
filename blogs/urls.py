from django.urls import path

from blogs import apis
from blogs.views import (
    BlogIndexView,
    BlogCreateView,
    BlogDetailView,
    BlogUpdateView,
    BlogDeleteView,
)

app_name = "blogs"

urlpatterns = [
    path("", BlogIndexView.as_view(), name="index"),
    path("create/", BlogCreateView.as_view(), name="create"),
    path("<int:pk>/", BlogDetailView.as_view(), name="detail"),
    path("update/<int:pk>/", BlogUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", BlogDeleteView.as_view(), name="delete"),
    # like
    path("like/<int:blog_id>/", apis.get_like, name="get_like"),
    path("like/<int:blog_id>/toggle/", apis.toggle_like, name="toggle_like"),
]
