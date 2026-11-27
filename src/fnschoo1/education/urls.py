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
        views.TeacherListView.as_view(),
        name="list_teachers",
    ),
    path(
        "list_students",
        views.StudentListView.as_view(),
        name="list_students",
    ),
    path(
        "list_courses",
        views.CourseListView.as_view(),
        name="list_courses",
    ),
    path(
        "list_teacher_leaves",
        views.TeacherLeaveListView.as_view(),
        name="list_teacher_leaves",
    ),
]

# The end.
