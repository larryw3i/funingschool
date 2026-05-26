from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "fnhome"

urlpatterns = [
    path("home", views.home, name="home"),
    path("", views.home, name="home"),
    path("service_terms", views.service_terms, name="service_terms"),
]

# The end.
