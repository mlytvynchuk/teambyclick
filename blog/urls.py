from django.urls import path, include
from .views import blog, blog_detail

urlpatterns = [
    path("", blog, name="blog"),
    path("<int:id>/", blog_detail, name="blog_detail"),
]
