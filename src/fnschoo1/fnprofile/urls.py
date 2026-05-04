from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "fnprofile"

urlpatterns = [
    path("view_profile", views.edit_fnprofile, name="view_profile"),
    path("log_out", views.fnprofile_log_out, name="log_out"),
    path("new_profile", views.new_fnprofile, name="new_profile"),
    path("log_in", views.fnprofile_log_in, name="log_in"),
    path("edit_profile", views.edit_fnprofile, name="edit_profile"),
    path("emails", views.list_emails, name="list_emails"),
    path("new_email", views.new_email, name="new_email"),
    path("view_email/<uuid:email_id>", views.view_email, name="view_email"),
    path(
        "edit_email/<uuid:email_id>",
        views.edit_email,
        name="edit_email",
    ),
    path(
        "delete_email/<uuid:email_id>", views.delete_email, name="delete_email"
    ),
]
# The end.
