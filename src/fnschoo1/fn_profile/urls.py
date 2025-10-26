from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "fn_profile"

urlpatterns = [
    path("detail", views.fn_profile_edit, name="detail"),
    path("log_out", views.fn_profile_log_out, name="log_out"),
    path("create", views.fn_profile_new, name="create"),
    path("log_in", views.fn_profile_log_in, name="log_in"),
    path("update", views.fn_profile_edit, name="update"),
]
# The end.
