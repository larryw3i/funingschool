from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "education"

urlpatterns = [
    path(
        "edit_student_profile",
        views.edit_student_profile,
        name="edit_student_profile",
    ),
    path(
        "edit_teacher_profile",
        views.edit_teacher_profile,
        name="edit_teacher_profile",
    ),
    path(
        "list_teachers",
        views.list_teachers,
        name="list_teachers",
    ),
    path(
        "list_students",
        views.list_students,
        name="list_students",
    ),
]

# The end.
