# apps/news/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("digest-preview/", views.digest_preview, name="digest-preview"),
]
