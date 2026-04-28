from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "fnprofile"

urlpatterns = [
    path("detail", views.fnprofile_edit, name="detail"),
    path("log_out", views.fnprofile_log_out, name="log_out"),
    path("create", views.fnprofile_new, name="create"),
    path("log_in", views.fnprofile_log_in, name="log_in"),
    path("update", views.fnprofile_edit, name="update"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("emails", views.email_list, name="email_list"),
    path("emails/add", views.email_add, name="email_add"),
    path("emails/<uuid:email_id>", views.email_detail, name="email_detail"),
    path("emails/<uuid:email_id>/edit", views.email_edit, name="email_edit"),
    path(
        "emails/<uuid:email_id>/verify/<str:token>",
        views.email_verify,
        name="email_verify",
    ),
    path(
        "emails/<uuid:email_id>/verify",
        views.email_verify,
        name="email_verify_form",
    ),
    path(
        "emails/<uuid:email_id>/resend",
        views.email_resend_verification,
        name="email_resend_verification",
    ),
    path(
        "emails/<uuid:email_id>/toggle",
        views.email_toggle_status,
        name="email_toggle_status",
    ),
    path(
        "emails/<uuid:email_id>/set-primary",
        views.email_set_primary,
        name="email_set_primary",
    ),
    path(
        "emails/<uuid:email_id>/delete", views.email_delete, name="email_delete"
    ),
]
# The end.
